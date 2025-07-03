import requests
import logging
from odoo import tools

_logger = logging.getLogger(__name__)

class WebServiceClient:

    # URL del servicio web para recibir la actualización de productos
    ENDPOINT = "https://servicios.farmapagos.app/api/producto/actualizar"
    API_KEY = None  # Si se usa token (puedes cargarlo con ir.config_parameter)

    @classmethod
    def send_product_update(cls, product):
        try:
            payload = {
                "id": product.id,
                "codigoProducto": product.default_code or "",
                "sku": product.default_code,
                "nombre": product.name or "",
                "moneda": None,
                "precio": product.standard_price or 0,
                "momnedaPrecioVenta": None,
                "precioVenta": product.list_price or 0,
                "anillo": None,
                "codigoHub": product.product_tmpl_id.x_studio_codigo_hub if hasattr(product.product_tmpl_id, 'x_studio_codigo_hub') else None,
                "codigoFarmacia": product.product_tmpl_id.x_studio_codigo_farmacia if hasattr(product.product_tmpl_id, 'x_studio_codigo_farmacia') else None,
                "tiempoMinutos": None,
                "existencia": product.qty_available,
                "fechaCreacion": product.create_date.isoformat() if product.create_date else None,
                "fechamodificacion": product.write_date.isoformat() if product.write_date else None,
                "idPais": None,
                "simboloMoneda": product.currency_id.symbol if product.currency_id else None,
                "descripcion": product.description_sale or "",
                "url_imagen": f"/web/image/product.template/{product.product_tmpl_id.id}/image_1920" if product.product_tmpl_id.image_1920 else None,
                "receta": None,
                "promovido": None,
                "porcentajedescuento": None,
                "montoDescuento": None,
                "etiquetaimpuesto": ", ".join(t.name for t in product.taxes_id) if product.taxes_id else "",
                "montoImpuesto": None,
                "precioOriginal": product.list_price or 0
            }

            headers = {
                "Content-Type": "application/json"
            }
            if cls.API_KEY:
                headers["Authorization"] = f"Bearer {cls.API_KEY}"

            response = requests.post(cls.ENDPOINT, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                _logger.info("Producto %s enviado correctamente al servicio externo.", product.default_code)
            else:
                _logger.warning("Error HTTP al enviar producto %s: %s", product.default_code, response.text)

        except Exception as e:
            _logger.error("Error al enviar producto %s al servicio: %s", product.default_code, str(e))

    @classmethod
    def notify_product_deletion(cls, product):
        if not product.default_code:
            _logger.warning("Producto sin código no puede ser eliminado del servicio.")
            return

        url = "https://servicios.farmapagos.app/api/producto/eliminar"
        payload = {"codigoProducto": product.default_code}

        headers = {"Content-Type": "application/json"}
        if cls.API_KEY:
            headers["Authorization"] = f"Bearer {cls.API_KEY}"  # si aplica

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                _logger.info("Producto eliminado en servicio externo: %s", product.default_code)
            else:
                _logger.warning("Fallo al eliminar producto %s: %s", product.default_code, response.text)
        except Exception as e:
            _logger.error("Error notificando eliminación: %s", str(e))
