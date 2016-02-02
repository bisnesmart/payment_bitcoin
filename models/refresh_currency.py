# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2009 CamptoCamp. All rights reserved.
#    @author Nicolas Bessi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api, _
from openerp import exceptions
from openerp.addons.currency_rate_update.services.currency_getter import Currency_getter_factory


_logger = logging.getLogger(__name__)

class Currency_rate_update_service(models.Model):
    """Class keep services and currencies that
    have to be updated"""

    _inherit = "currency.rate.update.service"
    _description = "Currency Rate Update"

    @api.one
    def refresh_currency_btc(self):
        """Refresh the BTC rates !!for all companies now"""
        _logger.info(
            'Starting to refresh currencies with service %s (company: %s)',
            self.service, self.company_id.name)
        factory = Currency_getter_factory()
        curr_obj = self.env['res.currency']
        rate_obj = self.env['res.currency.rate']
        company = self.company_id
        # The multi company currency can be set or no so we handle
        # The two case
        if company.auto_currency_up:
            main_currency = curr_obj.search(
                [('base', '=', True), ('company_id', '=', company.id)],
                limit=1)
            if not main_currency:
                # If we can not find a base currency for this company
                # we look for one with no company set
                main_currency = curr_obj.search(
                    [('base', '=', True), ('company_id', '=', False)],
                    limit=1)
            if not main_currency:
                raise exceptions.Warning(_('There is no base currency set!'))
            if main_currency.rate != 1:
                raise exceptions.Warning(_('Base currency rate should '
                                           'be 1.00!'))
            note = self.note or ''
            try:
                # We initalize the class that will handle the request
                # and return a dict of rate
                getter = factory.register(self.service)
                curr_to_fetch = map(lambda x: x.name,
                                    self.currency_to_update)
                res, log_info = getter.get_updated_currency(
                    curr_to_fetch,
                    main_currency.name,
                    self.max_delta_days
                    )
                rate_name = \
                    fields.Datetime.to_string(datetime.utcnow().replace(
                        hour=0, minute=0, second=0, microsecond=0))
                for curr in self.currency_to_update:
                    if curr.id == main_currency.id:
                        continue
                    do_create = True
                    for rate in curr.rate_ids:
                        if rate.name == rate_name:
                            rate.rate = res[curr.name]
                            do_create = False
                            break
                    if do_create:
                        vals = {
                            'currency_id': curr.id,
                            'rate': res[curr.name],
                            'name': rate_name
                        }
                        rate_obj.create(vals)
                        _logger.info(
                            'Updated currency %s via service %s',
                            curr.name, self.service)

                # Show the most recent note at the top
                msg = '%s \n%s currency updated. %s' % (
                    log_info or '',
                    fields.Datetime.to_string(datetime.today()),
                    note
                )
                self.write({'note': msg})
            except Exception as exc:
                error_msg = '\n%s ERROR : %s %s' % (
                    fields.Datetime.to_string(datetime.today()),
                    repr(exc),
                    note
                )
                _logger.error(repr(exc))
                self.write({'note': error_msg})
            if self._context.get('cron', False):
                midnight = time(0, 0)



    @api.multi
    def run_currency_update_btc(self):
        # Update currency at the given frequence
        services = self.search([('next_run','!=', False)])
        services.refresh_currency_btc()
    @api.model
    def _run_currency_update_btc(self):
        _logger.info('Starting rate update BTC')
        self.run_currency_update_btc()
        _logger.info('End of the currency rate update BTC')
