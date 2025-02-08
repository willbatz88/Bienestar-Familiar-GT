import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"  # Extendemos el modelo de albaranes

    referencia_externa = fields.Char(string="Referencia Externa", help="Campo para almacenar una referencia externa")

    def confirmar_y_notificar(self):
        """
        Método personalizado que cambia el estado a 'done' y notifica al usuario
        """
        for picking in self:
            if picking.state not in ['confirmed', 'assigned']:
                raise UserError("El albarán debe estar en estado 'Confirmado' o 'Reservado' para completarlo.")

            # Cambiar el estado del albarán a 'hecho'
            picking.button_validate()

            # Registrar en el log
            _logger.info(f"Albarán {picking.name} confirmado y notificado.")

            # Enviar una notificación al usuario
            picking.message_post(
                body=f"El albarán <b>{picking.name}</b> ha sido confirmado y completado.",
                message_type="notification"
            )

        return True