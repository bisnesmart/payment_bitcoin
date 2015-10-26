
# -*- coding: utf-8 -*-

from openerp.addons.payment.models.payment_acquirer import ValidationError
#from openerp.addons.payment_bitcoin.controllers.main import OgoneController
from openerp.osv import osv, fields
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _

import logging
import pprint

_logger = logging.getLogger(__name__)

class AcquirerPaymentBitcoin(osv.Model):

	_inherit = 'payment.acquirer'

	_columns ={

		'bitcoin_address': fields.char('Bitcoin address')

	}

	#TODO: Enlazar con servidor rpc
	# bitcoin_rpc_server = fields.Char('Bitcoin Server rpc')
	# bitcoin_rpc_port = fields.Char('Port server rpc')
	# bitcoin_rpc_username = fields.Char('User rpc')
	# bitcoin_rpc_password = fields.Char('Passwords rpc')

	def _get_providers(self, cr, uid, context=None):
		providers = super(AcquirerPaymentBitcoin, self)._get_providers(cr, uid, context=context)
		providers.append(['bitcoin', 'Bitcoin'])
		return providers
	def bitcoin_get_form_action_url(self, cr, uid, id, context=None):
		return '/payment/bitcoin/feedback'

	def _format_bitcoin_data(self, cr, uid, context=None):
		post_msg = '''<div>
<h3>Scan QR</h3>
<h4>Communication</h4>
<p>Please use the order name as communication reference.</p>
</div>'''
		return post_msg
	
	def create(self, cr, uid, values, context=None):
		""" Hook in create to create a default post_msg. This is done in create
		to have access to the name and other creation values. If no post_msg
		or a void post_msg is given at creation, generate a default one. """
		if values.get('provider') == 'bitcoin' and not values.get('post_msg'):
			values['post_msg'] = self._format_bitcoin_data(cr, uid, context=context)
		return super(AcquirerPaymentBitcoin, self).create(cr, uid, values, context=context)



class BitcoinPaymentTransaction(osv.Model):

 	_inherit = 'payment.transaction'

	def _bitcoin_form_get_tx_from_data(self,cr, uid, data, context=None):
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