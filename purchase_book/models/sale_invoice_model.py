# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Sale_Invoice_Book(models.Model):

    _name = "invoice.sale"
    _inherit = "mail.thread"
    _description = "Facturas Importadas para el Libro de Ventas"

    active = fields.Boolean('Activo', default=True)
    name = fields.Char('Nombre')
    fecha_documento = fields.Date(string="Fecha de Factura", tracking=True)
    codigo = fields.Selection([('1','Compras'), ('2','Bienes'), ('3','Exportaciones'),('4','Ventas Exentas'), ('5','Nota de Debito')], string="Codigo")
    cliente_id = fields.Many2one('res.partner', string="Nombre", domain=[('customer_rank', '=', 1)], tracking=True )
    nit = fields.Char(related='cliente_id.vat', string="NIT")
    serie_factura = fields.Char('Serie de Factura', tracking=True)
    no_factura= fields.Char('Numero de Factura', tracking=True)

    bienes = fields.Monetary("Bienes", compute='_compute_bienes', tracking=True)
    servicios = fields.Monetary("Servicios", compute='_compute_services', tracking=True)
    exportaciones = fields.Monetary('Exportaciones', compute='_compute_exportaciones', tracking=True)
    ventas = fields.Monetary('Ventas no Afectas', compute='_compute_ventas', tracking=True)
    iva = fields.Monetary("IVA", compute='_compute_iva', tracking=True)
    total = fields.Monetary("Total", tracking=True)
    invoice_state = fields.Selection([('draft', 'Borrador'), ('progress','En Proceso'), ('confirmed','Confirmado')], default="draft", string="Estado", tracking=True)

    company_id = fields.Many2one('res.company', string='Empresa', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    @api.depends("total", "codigo")
    def _compute_bienes(self):
        for rec in self:
            if(rec.codigo =="1"):
                rec['bienes'] = rec.total/1.12
            else:
                rec['bienes'] = 0

    @api.depends("codigo", "total")
    def _compute_services(self):
        for rec in self:
            if(rec.codigo=="2"):
                rec['servicios'] = rec.total /1.12
            else:
                rec['servicios'] = 0


    @api.depends("codigo", "total")
    def _compute_exportaciones(self):
        for rec in self:
            if(rec.codigo=="3"):
                rec["exportaciones"] = rec.total/1.12
            else:
                rec["exportaciones"] = 0

    @api.depends("codigo", "total")
    def _compute_ventas(self):
        for rec in self:
            if(rec.codigo=="4"):
                rec["ventas"] = rec.total/1
            else:
                rec["ventas"] = 0
    
    @api.depends("servicios", "bienes", "exportaciones")
    def _compute_iva(self):
        for rec in self:
                rec["iva"] = (rec.servicios + rec.bienes + rec.exportaciones)*0.12

    


        
