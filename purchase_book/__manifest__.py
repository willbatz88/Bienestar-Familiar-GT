# -*- coding: utf-8 -*-
{
    'name': "Libro de Compras",

    'summary': "Implementacion de Libro de Compras para Medicatel",

    'author': "Somos Moa",
    'website': "https://somosmoa.net/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'base',
                'base_automation', 
                'report_xlsx', 
                'mail',
                'account',
                'hr_expense'
                ],

    # always loaded
    'data': [
        'security/Invoice/ir.model.access.csv',
        'security/Book/ir.model.access.csv',
        'security/InvoiceSale/ir.model.access.csv',
        'security/BookSale/ir.model.access.csv',

        'views/book_menu.xml',
        'views/book_model.xml',
        'views/sale_book_model.xml',
        'report/purchase_report.xml',
        'report/sale_report.xml'
    ],
}