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
    @http.route('/recuperarOrden', auth='public', type='http', csrf=False, methods=['POST'])
    def recuperarOrder(self, **kwargs):
        requests = request.httprequest.data.decode()
        data = json.loads(requests)
        client =  request.env['res.partner'].sudo().search([('id', '=', data.get('nit'))])
        if not client:
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
        try: 
            order_lines = data.get('order_lines')
        #2	 	TORRE_TIGO
        #4	 	Forum Zona Viva
        #9	 	V1_FONTABELLA
        #10	 	V2_AVIA
        #11	 	V3_UFM
        #12	 	V4_URL
        #13	 	V6_UVG
        #14     unis
            idVending=data.get("idVending")
            valor=10
            if(idVending=="2"):
                valor=115 
            if(idVending=="4"):
                valor=117
            if(idVending=="9"):
                valor=8
            if(idVending=="10"):
                valor=9
            if(idVending=="11"):
                valor=25
            if(idVending=="12"):
                valor=12
            if(idVending=="13"):
                valor=11
            if(idVending=="14"):
                valor=13
            objetojson={str(valor):100}
            order = request.env['sale.order'].sudo().create({
                'partner_id': client.id,
                'partner_invoice_id': client.id,
                'partner_shipping_id': client.id,
                'pricelist_id': 1,
                'company_id': 37,
                'x_studio_serie': data.get('serie'),
                'x_studio_numero':data.get('number'),
                'date_order':data.get('fecha'),
                'currency_id':'167',
                'user_id':2,
            })
            for line in order_lines:
                idproducto =  request.env['product.product'].sudo().search([('default_code', '=', line.get('product_id'))])
                request.env['sale.order.line'].sudo().create({
                    'order_id': order.id,
                    'product_id': idproducto.id,
                    'name':line.get('name'),
                    'product_uom' : 1, 
                    'analytic_distribution':objetojson,
                    'product_uom_qty': line.get('product_uom_qty'),
                })        
            order_update = request.env['sale.order'].sudo().browse(order.id)
            if order_update:
                try:
                    order_update.action_confirm()
                    order_update.write({
                            'date_order':data.get('fecha')
                        })
                    invoices = order_update._create_invoices()
                    invoice = order_update.invoice_ids  # Esto devuelve un recordset de facturas relacionadas
                    _logger.info('%s',invoice)
                    invoices.action_post()
                    response_data = {"finalizado":"hecho"}
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
        except Exception as e:
            return self._error_response("Error al crear el pedido de venta: {}".format(str(e)))