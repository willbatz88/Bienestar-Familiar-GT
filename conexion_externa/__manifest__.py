{
    "name": "Módulo WebService para Odoo 16",
    "version": "16.0.1.0.0",
    "summary": "Envía transferencias de inventario a un WebService",
    "author": "willim Batz/ Bienestar Familiar",
    "depends": ["base", "stock", "mail"],  # Se añade 'mail' para seguimiento
    "data": [
        "security/ir.model.access.csv",  # Si necesitas definir permisos
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
