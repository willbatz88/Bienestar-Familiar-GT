# __manifest__.py
{
    'name': 'Consolidacion',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Gestion de Ejecuciones de Consolidacion',
    'description': """
        Aplicacion para gestionar las ejecuciones en el proceso de consolidacion.
    """,
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ejecucion_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}