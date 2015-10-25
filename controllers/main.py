# -*- coding: utf-8 -*-
import logging
import json
import pprint
import werkzeug

from openerp import http
from openerp.http import request


_logger = logging.getLogger(__name__)


class BitcoinController(http.Controller):
	
	_return_url = '/payment/bitcoin/feedback'

	def _get_return_url(self,**post):
		return_url = post.pop('return_url', '')
		return returns_url



	@http.route(['/payment/bitcoin/feedback'], type='http', auth='none', metods=['POST'])

	def bitcoin_feedback(self, **post):
		return_url = self._get_return_url(**post)
	 	_logger.info('Beginning form_feedback with post data %s', pprint.pformat(post))  # debug
	 	request.registry['payment.transaction'].form_feedback(cr, uid, post, 'bitcoin', context)

	 	return werkzeug.utils.redirect(return_url)