import requests
import json
from odoo import models, fields, api

class WebServiceConnector(models.Model):
    _name = "web.service.connector"
    _description = "Conector para enviar transferencias a un WebService"

    @api.model
    def enviar_transferencia(self, picking_id):
        picking = self.env["stock.picking"].browse(picking_id)
        
        # Datos de la transferencia
        datos_transferencia = {
            "id": picking.id,
            "origen": picking.location_id.display_name,
            "destino": picking.location_dest_id.display_name,
            "fecha": picking.scheduled_date.strftime("%Y-%m-%d %H:%M:%S"),
            "estado": picking.state,
            "productos": [
                {
                    "producto": line.product_id.display_name,
                    "cantidad": line.quantity_done
                } for line in picking.move_line_ids
            ]
        }

        # URL del servicio
        url = "https://api.ejemplo.com/transferencias"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer TU_TOKEN_AQUI"
        }

        # Enviar solicitud
        response = requests.post(url, json=datos_transferencia, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Error en la solicitud: {response.status_code} - {response.text}")

        return response.json()
