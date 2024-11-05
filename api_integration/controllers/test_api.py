# -*- coding: utf-8 -*-
import json
import logging
from odoo import http, _
from odoo.exceptions import UserError
from odoo.http import Response, request
from odoo.exceptions import AccessError, MissingError
import yaml
_logger = logging.getLogger(__name__)

class TestApi(http.Controller):
    @http.route('/createOrder', auth='public', type='http', csrf=False, methods=['POST'])
    def createOrder(self, **kwargs):
        requests = request.httprequest.data.decode()
        data = json.loads(requests)
        #client =  request.env['res.partner'].sudo().search([('id', '=', data.get('partner_id'))])

        #if not client:
        #        return self._error_response("El cliente no existe.")

        client = request.env['res.partner'].sudo().create({
                'name': data.get('name'),
                'city': 'Guatemala',
                'vat': data.get('nit'),
                'customer_rank': 1,
                'company_type': 'person',
                'property_account_receivable_id': 1434,
                'property_account_payable_id': 783,
                'company_id': 37,
                'lang':'es_ES'
                })
        
        #company =  request.env['res.company'].sudo().search([('company_registry', '=', data['company_registry'])])

        #if not company:
            #            return self._error_response("La Empresa indicada no existe.")
        
        try: 
            #required_fields = ['partner_id', 'company_registry', 'order_lines']
            #for field in required_fields:
            #    if field not in data or not data.get(field):
            #        return self._error_response("Falta el campo '{}' o está vacío.".format(field))
               
            #partner_id = data.get('partner_id')
            #partner_invoice_id = data.get('partner_id')
            #partner_shipping_id = data.get('partner_id')
            #pricelist_id = 2
            #company_id = data['company_registry']
            order_lines = data.get('order_lines')
            #additional_information = data.get('additional_information')

            order = request.env['sale.order'].sudo().create({
                'partner_id': client.id,
                'partner_invoice_id': client.id,
                'partner_shipping_id': client.id,
                'pricelist_id': 1,
                'company_id': 37,
               # 'x_studio_factura_externa': payment_id,
                #'x_studio_estado':'Colocado',
                #'x_studio_forma_de_pago':data.get('formadepago'),
                #'x_studio_total_farmapagos':data.get('montoFarmapago'),
                #'x_studio_total_efectivo':data.get('montoEfectivo'),
                #'x_studio_total_vuelto':data.get('montoVuelto'),
                #'x_studio_total_texto':data.get('texto_monto'),
                #'x_studio_entrega':data.get('entrega'),
                #'x_studio_fecha_entrega':data.get('fecha_entrega'),
                #'x_studio_direccion_final':data.get('direccion_final'),
                'currency_id':'167',
                'user_id':2,
            })
        
            _logger.info('%s',order.id)

            #for line in additional_information:
             #   request.env['order.additional_information'].sudo().create({
             #       'sale_order_id' : order.id,
              #      'label' : line.get('label'),
               #     'area' : line.get('area'),
               #     'value' : line.get('value')
               # })

            for line in order_lines:
                request.env['sale.order.line'].sudo().create({
                    'order_id': order.id,
                    'product_id': line.get('product_id'),
                    'name':line.get('name'),
                    'product_uom' : 1, 
                    'product_uom_qty': line.get('product_uom_qty'),
                })
            
            order_update = request.env['sale.order'].sudo().browse(order.id)
            _logger.info('%s',order_update)
            if order_update:
                try:
                    order_update.action_confirm()
                    #return self._success_response("Generacion de Pedido de Venta")
                    response_data = {"finalizado":"hecho"}
                                      #  request.env['mail.activity'].sudo().create({
                  #      'display_name': 'Venta Nueva',
                  #      'summary': 'Hay una venta Nueva que atender',
                  #      'user_id': 2,
                  #      'res_id': order.id,
                  #      'res_model_id': 620,
                  #      'activity_type_id': 4
                  # })
                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers=[("Cache-Control", "no-store"),("Pragma", "no-cache")],
                        response = json.dumps(response_data)
                        )
                
                except Exception as e :
                    return self._error_response(f"Error al establecer el estado Pedido de Venta {str(e)}")
            else:
                 return self._error_response("Registro no encontrado.")
        
            #return self._success_response("Datos en la peticion")
        except Exception as e:
            return self._error_response("Error al crear el pedido de venta: {}".format(str(e)))
    
    
   