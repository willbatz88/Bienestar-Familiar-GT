# __manifest__.py
{
    'name': 'Consolidacion',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Gestion de Ejecuciones de Consolidacion',
    'description': '',
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ejecucion_menu.xml',
        'views/ejecucion_views.xml',
    ],
    'installable': True,
    'application': True,

}