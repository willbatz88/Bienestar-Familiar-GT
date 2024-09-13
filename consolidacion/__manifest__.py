# __manifest__.py
{
    'name': 'Consolidación',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Módulo para la consolidación de ejecuciones',
    'description': """
        Este módulo permite gestionar las ejecuciones en el proceso de consolidación.
    """,
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'depends': ['base'],  # Dependencias del módulo, puedes agregar más si es necesario
    'data': [
        'security/ir.model.access.csv',  # Seguridad y permisos
        'views/ejecucion_views.xml',     # Vistas XML
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}