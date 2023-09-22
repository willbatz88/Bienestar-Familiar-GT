# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
class hr_expense_inherit(models.Model):
    _inherit="hr.expense"

    codigo = fields.Selection([('1','Compras'), ('2','Servicios'), ('3','Combustible'),('4','Pequeño Contribuyente'), ('5','Factura Especial')], string="Codigo")
    tipo_documento = fields.Selection([('fc','Factura'), ('fce','Factura Electronica'), ('fpq','Factura Pequeño Contribuyente'),('fe','Factura Especial')], string="Tipo de Documento")

    no_serie= fields.Char('No. de Serie')
    proveedor= fields.Many2one('res.partner', string="Proveedor")
    tasa_municipal = fields.Monetary('Tasa Municipal')
    timbre_prensa = fields.Monetary('Timbre de Prensa')
    turismo_hospedaje = fields.Monetary('Turismo por Hospedaje')
    idp =  fields.Monetary('IDP')
    comentario = fields.Char('Comentario')

    #@api.model
    def create_purchase(self):
        for rec in self:
                purchase = self.env['invoice.purchase']
                new = purchase.create({
                    'fecha_documento': rec.date,
                    'no_factura': rec.reference,
                    'codigo': rec.codigo,
                    'tipo_documento': rec.tipo_documento,
                    'proveedor_id': rec.proveedor.id,
                    'serie_factura': rec.no_serie,
                    'total': rec.total_amount,
                    'tasa_municipal': rec.tasa_municipal,
                    'timbre_prensa': rec.timbre_prensa,
                    'turismo_hospedaje': rec.turismo_hospedaje,
                    'idp': rec.idp
                })

    
class hr_expense_sheet_expense(models.Model):
    _inherit="hr.expense.sheet"

    def _prepare_move_vals(self):
        invoice_vals = super(hr_expense_sheet_expense,self)._prepare_move_vals()
        invoice_vals['codigo'] = self.expense_line_ids.codigo
        invoice_vals['tipo_documento'] = self.expense_line_ids.tipo_documento
        invoice_vals['serie_factura'] = self.expense_line_ids.no_serie
        invoice_vals['comment'] = self.expense_line_ids.comentario
        return invoice_vals


