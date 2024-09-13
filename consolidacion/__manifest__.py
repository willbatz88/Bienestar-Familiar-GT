# __manifest__.py
{
    'name': 'Consolidación',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Gestión de Ejecuciones de Consolidación',
    'description': """
        Aplicación para gestionar las ejecuciones en el proceso de consolidación.
    """,
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ejecucion_views.xml',
    ],
    'installable': True,
    'application': True,  # Indica que es una aplicación
    'auto_install': False,
}