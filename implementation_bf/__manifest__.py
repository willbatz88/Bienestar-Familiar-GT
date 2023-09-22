# -*- coding: utf-8 -*-
{
    'name': "Implementacion BF",

    'summary': "",

    'author': "Somos Moa",
    'website': "https://somosmoa.net/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'report_xlsx'],

    # always loaded
    'data': [

        #'reports/libro_diario_report.xml',
        'security/ir.model.access.csv',
        'reports/new_report.xml',

        'wizard/generate_book_view.xml',

        'views/libro_diario.xml'
    ],
}