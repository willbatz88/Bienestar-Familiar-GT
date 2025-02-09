import logging
import requests
import json 
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"  # Extendemos el modelo de albaranes

    def confirmar_y_notificar(self):
        _logger.info(f"Albarán confirmado y notificado.")
        # Definir la URL del servicio web
        url = "http://busservicio-dev.eba-epxjazui.us-east-1.elasticbeanstalk.com/api/IntegrateSrFrm/pruebaConexion?cadena=1&nombre=desdeOtraUbicacion'"
        #datos_transferencia = {
        #    "id": record.id,
        #    "origen": record.location_id.display_name,
        #    "destino": record.location_dest_id.display_name,
        #    "fecha": record.scheduled_date.strftime("%Y-%m-%d %H:%M:%S"),
        #    "estado": record.state,
        #    "productos": [
        #        {
        #            "producto": line.product_id.display_name,
        #            "cantidad": line.quantity_done
        #        } for line in record.move_line_ids
        #    ]
        #}
        response=requests.get(url)
        #response = requests.post(url, data=json.dumps(datos_transferencia))
        # Verificar la respuesta
        if response.status_code != 200:
            raise Exception(f"Error en la solicitud: {response.status_code} - {response.text}")
        return True