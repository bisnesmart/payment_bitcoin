
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
		return '/payment/bitcoin/feedback'

	def _format_bitcoin_data(self, cr, uid, context=None):
		post_msg = '''<div>
		<h3>Please use the following transfer details</h3>
		<h4>Ya queda poco</h4>
		<h4>Communication</h4>
		<p>Please use the order name as communication reference.</p>
		</div>'''
		return post_msg

	# def create(self, cr, uid, values, context=None):
	# 	""" Hook in create to create a default post_msg. This is done in create
	# 	to have access to the name and other creation values. If no post_msg
	# 	or a void post_msg is given at creation, generate a default one. """
	# 	if values.get('provider') == 'transfer' and not values.get('post_msg'):
 #            values['post_msg'] = self._format_transfer_data(cr, uid, context=context)
 #        return super(TransferPaymentAcquirer, self).create(cr, uid, values, context=context)


class BitcoinPaymentTransaction(models.Model):

 	_inherit = 'payment.transaction'

	def _bitcoin_form_get_tx_from_data(self,data,):
		reference, amount, currency_name = data.get('reference'), data.get('amount'), data.get('currency_name')
		tx_ids = self.search(
		cr, uid, [
			('reference', '=', reference),
		], context=context)

		if not tx_ids or len(tx_ids) > 1:
			error_msg = 'received data for reference %s' % (pprint.pformat(reference))
			if not tx_ids:
				error_msg += '; no order found'
			else:
				error_msg += '; multiple order found'
			_logger.error(error_msg)
			raise ValidationError(error_msg)

		return self.browse(cr, uid, tx_ids[0], context=context)

	def _bitcoin_form_validate(self, cr, uid, tx, data, context=None):
		_logger.info('Validated bitcoin payment for tx %s: set as pending' % (tx.reference))
		return tx.write({'state': 'pending'})