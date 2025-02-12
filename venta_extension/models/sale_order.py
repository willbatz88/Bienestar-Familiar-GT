import logging
import requests
import json 
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"  # Extendemos el modelo de albaranes
    def obtener_fecha_formateada():
    # Obtener la fecha actual
        
    # Convertir la fecha al formato deseado: 'yyyy-mm-dd'
        
        return fecha_formateada

    def action_mi_accion(self):
        _logger.info(f"Venta confirmado y notificado."+str(self.id))
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime("%Y-%m-%d")
        # Definir la URL del servicio web
        url = "https://srfarmacia.bf-transac.com/api/IntegrateSrFrm/NotificarVenta"
        lista=[]
        base=240
        for line in self.order_line:
            product = line.product_id
            producto= {
                    "product_id": base,
                    "name": product.name,
                    "product_uom_qty":str(line.product_uom_qty),
                    "product_uom":1,
                    "unit_cost":product.standard_price
                } 
            base=base+1
            lista.append(producto)

        datos_transferencia = {
            "picking_type_id": 1,
            "location_origin_id": 1,
            "location_dest_id": 1,
            "provider_id": 1,
            "payment_method_id": 1,
            "origin":"Bodega Central",
            "scheduled_date":fecha_formateada,
            "id_sistema_origen":self.name,
            "invoice":"32323",
            "serie":"234234234",
            "moves":lista
        }
        headers = {"Content-Type": "application/json"}
        #response=requests.get(url)
        response = requests.post(url, data=json.dumps(datos_transferencia),headers=headers)
        # Verificar la respuesta
        _logger.info("codigo: "+str(response.status_code))
        if response.status_code != 200:
            raise Exception(f"Error en la solicitud: {response.status_code} - {response.text}")
        
        return True