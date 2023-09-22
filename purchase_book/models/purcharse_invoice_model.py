# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Purchase_Book(models.Model):

    _name = "invoice.purchase"
    _inherit = "mail.thread"
    _description = "Facturas Importadas para el Libro de Compras"

    active = fields.Boolean('Activo', default=True)
    exento = fields.Boolean('Compra Exenta', default=False)
    name= fields.Char("Nombre")
    fecha_documento = fields.Date(string="Fecha de Documento", tracking=True)
    no_factura= fields.Char('Numero de Factura', tracking=True)
    codigo = fields.Selection([('1','Compras'), ('2','Servicios'), ('3','Combustible'),('4','Pequeño Contribuyente'), ('5','Factura Especial'), ('6', 'Nota de Credito')], string="Codigo")
    tipo_documento = fields.Selection([('fc','Factura'), ('fce','Factura Electronica'), ('fpq','Factura Pequeño Contribuyente'),('fe','Factura Especial'), ('nc', 'Nota de Credito')], string="Tipo de Documento")
    proveedor_id = fields.Many2one('res.partner', string="Nombre", domain=[('supplier_rank', '=', 1)], tracking=True )
    nit = fields.Char(related='proveedor_id.vat', string="NIT")
    serie_factura = fields.Char('Serie de Factura', tracking=True)

    compras = fields.Monetary("Compras", compute='_compute_purchase', tracking=True)
    servicios = fields.Monetary("Servicios", compute='_compute_services', tracking=True)
    compras_genericas = fields.Monetary("Compras Genericas", tracking=True)
    tasa_municipal = fields.Monetary('Tasa Municipal', tracking=True)
    timbre_prensa = fields.Monetary('Timbre de Prensa')
    turismo_hospedaje = fields.Monetary('Turismo por Hospedaje', tracking=True)
    idp =  fields.Monetary('IDP', tracking=True)
    combustible = fields.Monetary('Combustible', compute='_compute_combustible', tracking=True)
    fac_fpq = fields.Monetary("Fac. Pequeño Contribuyente", compute='_compute_fpq', tracking=True)
    factura_especial = fields.Monetary("Factura Especial", compute='_compute_especial_fac', tracking=True)
    iva_credito = fields.Monetary("IVA Credito", compute='_compute_iva', tracking=True)
    total = fields.Monetary("Total", tracking=True)
    invoice_state = fields.Selection([('draft', 'Borrador'), ('progress','En Proceso'), ('confirmed','Confirmado')], default="draft", string="Estado", tracking=True)

    company_id = fields.Many2one('res.company', string='Empresa', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    @api.depends("total", "codigo", "exento", "compras_genericas")
    def _compute_purchase(self):
        for rec in self:
            if(rec.codigo =="1" and rec.exento==False):
                rec['compras'] = rec.total/1.12
            elif(rec.codigo =="1" and rec.exento==True):
                rec['compras'] = (rec.total - rec.compras_genericas)/1.12
            else:
                rec['compras'] = 0

    @api.depends("codigo","tasa_municipal", "timbre_prensa", "turismo_hospedaje", "total")
    def _compute_services(self):
        for rec in self:
            if(rec.codigo=="2"):
                rec['servicios'] = (rec.total - (rec.tasa_municipal + rec.turismo_hospedaje + rec.timbre_prensa))/1.12
            else:
                rec['servicios'] = 0

    @api.depends("codigo", "total", "idp")
    def _compute_combustible(self):
        for rec in self:
            if(rec.codigo=="3"):
                rec["combustible"] = (rec.total - rec.idp)/1.12
            else:
                rec["combustible"] = 0

    @api.depends("codigo", "total")
    def _compute_fpq(self):
        for rec in self:
            if(rec.codigo=="4"):
                rec["fac_fpq"] = rec.total/1
            else:
                rec["fac_fpq"] = 0

    @api.depends("codigo", "total")
    def _compute_especial_fac(self):
        for rec in self:
            if(rec.codigo=="5"):
                rec["factura_especial"] = rec.total/1.12
            else:
                rec["factura_especial"] = 0

    @api.depends("total", "tipo_documento", "compras","servicios", "combustible")
    def _compute_iva(self):
        for rec in self:
            if(rec.tipo_documento=="FPQ"):
                rec["iva_credito"] = 0
            else:
                rec["iva_credito"] = (rec.compras + rec.servicios + rec.combustible) * 0.12


        
