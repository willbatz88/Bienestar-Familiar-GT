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
        url = "https://srfarmacia.bf-transac.com/api/IntegrateSrFrm/NotificarVenta"
        datos_transferencia = {
            "picking_type_id": 1,
            "location_origin_id": 1,
            "location_dest_id": 1,
            "provider_id": 1,
            "payment_method_id": 1,
            "origin":"Bodega Central",
            "scheduled_date":"2025-02-28",
            "id_sistema_origen":"Odoo-003",
            "invoice":"0",
            "serie":"0",
            "moves": [
                {
                    "product_id": 240,
                    "name": "[P017896] TYLENOL EXTRAFUERTE 500MG 20 CAPSULA (10 SOBRE X 2)",
                    "product_uom_qty":25,
                    "product_uom":1,
                    "unit_cost":10.00
                } 
            ]
        }
        headers = {"Content-Type": "application/json"}
        #response=requests.get(url)
        response = requests.post(url, data=json.dumps(datos_transferencia),headers=headers)
        # Verificar la respuesta
        _logger.info("codigo: "+str(response.status_code))
        if response.status_code != 200:
            raise Exception(f"Error en la solicitud: {response.status_code} - {response.text}")
        return True