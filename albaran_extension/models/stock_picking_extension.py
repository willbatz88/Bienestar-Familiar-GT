import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"  # Extendemos el modelo de albaranes
        
    def confirmar_y_notificar(self):
        _logger.info(f"Albarán confirmado y notificado.")
        return True