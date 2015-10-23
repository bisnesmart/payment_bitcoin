
# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AcquirerPaymentBitcoin(models.Model):

	_inherit = 'payment.acquirer'

	bitcoin_rpc_server = fields.Char('Bitcoin Server rpc')
	bitcoin_rpc_port = fields.Char('Port server rpc')
	bitcoin_rpc_username = fields.Char('User rpc')
	bitcoin_rpc_password = fields.Char('Passwords rpc')

	@api.model
	def _get_providers(self):
		providers = super(AcquirerPaymentBitcoin, self)._get_providers()
		providers.append(['bitcoin', 'Bitcoin'])
		return providers