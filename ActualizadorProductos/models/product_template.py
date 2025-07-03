from odoo import models
from ..services.web_client import WebServiceClient
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def create(self, vals):
        """Al crear una plantilla, notificamos al web service del nuevo producto variante."""
        record = super().create(vals)
        try:
            # En Odoo 18 usamos product_variant_ids (one2many); aquí seleccionamos la primera variante creada
            variant = record.product_variant_ids and record.product_variant_ids[0]
            if variant:
                WebServiceClient.send_product_update(variant)
        except Exception as e:
            _logger.error("Error al enviar nuevo producto %s: %s", record.name, e)
        return record

    def write(self, vals):
        """Al actualizar la plantilla, notificamos por cada variante afectada."""
        result = super().write(vals)
        for record in self:
            for variant in record.product_variant_ids:
                try:
                    WebServiceClient.send_product_update(variant)
                except Exception as e:
                    _logger.error("Error al enviar actualización de producto %s [%s]: %s", record.name, variant.id, e)
        return result

    def unlink(self):
        """Antes de borrar, notificamos la eliminación de cada variante."""
        for record in self:
            for variant in record.product_variant_ids:
                try:
                    WebServiceClient.notify_product_deletion(variant)
                except Exception as e:
                    _logger.error("Error notificando eliminación de producto %s [%s]: %s", record.name, variant.id, e)
        return super().unlink()
