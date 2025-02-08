import requests
import json
from odoo import models, fields, api
class webconnector(models.Model):
    _name = "webconnector"
    _description = "Conector para enviar transferencias a un WebService"
    response_message = fields.Text(string="Respuesta del Servidor")
    @api.model
    def enviar_transferencia(self, picking_id):
        try:
            url = "http://busservicio-dev.eba-epxjazui.us-east-1.elasticbeanstalk.com/api/IntegrateSrFrm/pruebaConexion?cadena=2&nombre=desdeendpoint"
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Error en la solicitud: {response.status_code} - {response.text}")
            return response.json()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Error al enviar la transferencia: %s") % str(e))
        return True;
         #picking = self.env["stock.picking"].browse(picking_id)
        
        # Datos de la transferencia
        #datos_transferencia = {
        #    "id": picking.id,
        #    "origen": picking.location_id.display_name,
        #    "destino": picking.location_dest_id.display_name,
        #    "fecha": picking.scheduled_date.strftime("%Y-%m-%d %H:%M:%S"),
        #    "estado": picking.state,
        #    "productos": [
        #        {
        #            "producto": line.product_id.display_name,
        #            "cantidad": line.quantity_done
        #        } for line in picking.move_line_ids
        #    ]
        #}
        #headers = {
        #    "Content-Type": "application/json",
        #    "Authorization": "Bearer TU_TOKEN_AQUI"
        #}
        # Enviar solicitud
#        response = requests.post(url, json=datos_transferencia, headers=headers)