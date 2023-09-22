# -*- coding: utf-8 -*-
{
    'name': "Sequences Bienestar Familiar",

    'summary': "Integracion de cambios en modulos base",

    'description': "Implementar cambios referentes a campos requeridos en los modulos base de Odoo",

    'author': "Somos Moa",
    'website': "https://somosmoa.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account', 'base_automation', 'sale_management', 'stock', 'hr', 'hr_expense', 'mail'],

    # always loaded
    'data': [
        'data/account_sequences.xml',
        'data/client_sequences.xml',
        'data/employee_sequences.xml',
        'data/store_sequences.xml',
        'data/supplier_sequences.xml',

        'data/expense_automate_action.xml',
        'data/debit_note_automate_action.xml',
        'data/purchase_automate_action.xml',
        'data/credit_note_automate_action.xml',
        'data/sale_automate_action.xml',
        
        'views/expense_inherit.xml',
        'views/account_inherit.xml',
        'views/sale_inherit.xml',
        'views/contacts_inherit.xml',
        'views/employee_inherit.xml',
        'views/store_inherit.xml',
    ],
}