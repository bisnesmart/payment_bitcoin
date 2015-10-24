
# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AcquirerPaymentBitcoin(models.Model):

	_inherit = 'payment.acquirer'

	bitcoin_address = fields.Char('Bitcoin address')
	#TODO: Enlazar con servidor rpc
	# bitcoin_rpc_server = fields.Char('Bitcoin Server rpc')
	# bitcoin_rpc_port = fields.Char('Port server rpc')
	# bitcoin_rpc_username = fields.Char('User rpc')
	# bitcoin_rpc_password = fields.Char('Passwords rpc')

	@api.model
	def _get_providers(self):
		providers = super(AcquirerPaymentBitcoin, self)._get_providers()
		providers.append(['bitcoin', 'Bitcoin'])
		return providers
	def transfer_get_form_action_url(self, cr, uid, id, context=None):
		return '/payment/transfer/feedback'


class BitcoinPaymentTransaction(models.Model):
 	_inherit = 'payment.transaction'

	def _bitcoin_form_get_tx_from_data(self, cr, uid, data, context=None):
		reference, amount, currency_name = data.get('reference'), data.get('amount'), data.get('currency_name')
		tx_ids = self.search(
		cr, uid, [
			('reference', '=', reference),
		], context=context)