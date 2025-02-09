import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"  # Extendemos el modelo de albaranes

    referencia_externa = fields.Char(string="Referencia Externa", help="Campo para almacenar una referencia externa")

    def confirmar_y_notificar(self):
        _logger.info(f"Albarán {picking.name} confirmado y notificado.")
        return True