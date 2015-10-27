# -*- coding: utf-8 -*-
{
    'name': "payment_bitcoin",

    'summary': """
        Bitcoin Payment Acquirer""",

    'description': """
        Bitcoin Payment Acquirer
    """,

    'author': "bisneSmart",
    'website': "http://www.bisneSmart.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'payment',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/payment_acquirer.xml',
        'views/confirmation.xml',
        'views/bitcoin.xml',
        'data/bitcoin.xml',
    ],
    'installable': True,
    
}