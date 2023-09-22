# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Shopping_Book(models.Model):

    _name="purchase.book"
    _inherit = "mail.thread"
    _description = "Creacion de Libro de Compras"

    active = fields.Boolean('Activo', default=True)

    fecha_libro = fields.Date(string="Fecha de Libro", tracking=True)
    name = fields.Char('Descripcion', tracking=True, required=True)

    company_id = fields.Many2one('res.company', string='Empresa', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    book_state = fields.Selection([('draft', 'Borrador'), ('progress','En Proceso'), ('paid','Pagado')], default="draft", string="Estado", tracking=True)

    qty_invoice = fields.Char('Cantidad de Facturas', compute='_compute_invoice_qty', store=True)
    compras = fields.Monetary("Compras", tracking=True, compute='_compute_invoice_compras', store=True)
    servicios = fields.Monetary("Servicios", tracking=True, compute='_compute_services', store=True)
    compras_genericas = fields.Monetary("Compras Genericas", tracking=True, compute='_compute_invoice_servicios_exentos', store=True)
    tasa_municipal = fields.Monetary("Tasa Municipal", tracking=True, compute='_compute_invoice_tasa_municipal', store=True)
    timbre_prensa = fields.Monetary("Timbre de Prensa", tracking=True, compute='_compute_invoice_timbre_prensa', store=True)
    turismo_hospedaje = fields.Monetary("Turismo por Hospedaje", tracking=True, compute='_compute_invoice_turismo_hospedaje', store=True)
    idp = fields.Monetary("IDP", tracking=True, compute='_compute_invoice_idp', store=True)
    combustible = fields.Monetary("Combustible", tracking=True, compute='_compute_invoice_combustible', store=True)
    fpq = fields.Monetary("Fac. de Pequeño Contribuyente", tracking=True, compute='_compute_invoice_fpq', store=True)
    factura_especial = fields.Monetary("Factura Especial", tracking=True, compute='_compute_invoice_factura_especial', store=True)
    iva_credito = fields.Monetary("IVA Credito", tracking=True, compute='_compute_invoice_iva_credito', store=True)
    total = fields.Monetary("Monto Total", tracking=True, compute='_compute_invoice_total', store=True)

    invoice_sheet_id = fields.Many2many('invoice.purchase')

    @api.depends("invoice_sheet_id")
    def _compute_invoice_qty(self):
        for rec in self:
            rec['qty_invoice']= len(rec.invoice_sheet_id.mapped('fecha_documento'))

    @api.depends("invoice_sheet_id")
    def _compute_invoice_total(self):
        for rec in self:
            rec['total']= sum(rec.invoice_sheet_id.mapped('total'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_compras(self):
        for rec in self:
            rec['compras']= sum(rec.invoice_sheet_id.mapped('compras'))
            
    @api.depends("invoice_sheet_id")
    def _compute_services(self):
        for rec in self:
            rec['servicios']= sum(rec.invoice_sheet_id.mapped('servicios'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_servicios_exentos(self):
        for rec in self:
            rec['compras_genericas']= sum(rec.invoice_sheet_id.mapped('compras_genericas'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_tasa_municipal(self):
        for rec in self:
            rec['tasa_municipal']= sum(rec.invoice_sheet_id.mapped('tasa_municipal'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_turismo_hospedaje(self):
        for rec in self:
            rec['turismo_hospedaje']= sum(rec.invoice_sheet_id.mapped('turismo_hospedaje'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_timbre_prensa(self):
        for rec in self:
            rec['timbre_prensa']= sum(rec.invoice_sheet_id.mapped('timbre_prensa'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_idp(self):
        for rec in self:
            rec['idp']= sum(rec.invoice_sheet_id.mapped('idp'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_combustible(self):
        for rec in self:
            rec['combustible']= sum(rec.invoice_sheet_id.mapped('combustible'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_fpq(self):
        for rec in self:
            rec['fpq']= sum(rec.invoice_sheet_id.mapped('fac_fpq'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_factura_especial(self):
        for rec in self:
            rec['factura_especial']= sum(rec.invoice_sheet_id.mapped('factura_especial'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_iva_credito(self):
        for rec in self:
            rec['iva_credito']= sum(rec.invoice_sheet_id.mapped('iva_credito'))
            
    
