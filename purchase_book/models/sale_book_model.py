# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Sale_Book(models.Model):

    _name="sale.book"
    _inherit = "mail.thread"
    _description = "Creacion de Libro de Ventas"

    active = fields.Boolean('Activo', default=True)

    fecha_libro = fields.Date(string="Fecha de Libro", required=True, tracking=True)
    name = fields.Char('Descripcion', tracking=True)
    #categoria = fields.Selection([('cruz_verde', 'CRUZ VERDE'), ('meykos', 'Meykos / Del Ahorro'), ('independiente', 'Independientes'), ('apomedix','Apomedix')], string="Categoria", tracking=True)

    company_id = fields.Many2one('res.company', string='Empresa', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    book_state = fields.Selection([('draft', 'Borrador'), ('progress','En Proceso'), ('paid','Pagado')], default="draft", string="Estado", tracking=True)

    qty_invoice = fields.Char('Cantidad de Facturas', compute='_compute_invoice_qty', store=True)
    bienes = fields.Monetary("bienes", tracking=True, compute='_compute_invoice_bienes', store=True)
    servicios = fields.Monetary("Servicios", tracking=True, compute='_compute_services', store=True)
    exportaciones = fields.Monetary("Exportaciones", tracking=True, compute='_compute_exportaciones', store=True)
    ventas = fields.Monetary("Ventas no Afectas", tracking=True, compute='_compute_ventas', store=True)
    iva = fields.Monetary("IVA", tracking=True, compute='_compute_invoice_iva', store=True)
    total = fields.Monetary("Monto Total", tracking=True, compute='_compute_invoice_total', store=True)

    invoice_sheet_id = fields.Many2many('invoice.sale')

    @api.depends("invoice_sheet_id")
    def _compute_invoice_qty(self):
        for rec in self:
            rec['qty_invoice']= len(rec.invoice_sheet_id.mapped('fecha_documento'))

    @api.depends("invoice_sheet_id")
    def _compute_invoice_total(self):
        for rec in self:
            rec['total']= sum(rec.invoice_sheet_id.mapped('total'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_bienes(self):
        for rec in self:
            rec['bienes']= sum(rec.invoice_sheet_id.mapped('bienes'))
            
    @api.depends("invoice_sheet_id")
    def _compute_services(self):
        for rec in self:
            rec['servicios']= sum(rec.invoice_sheet_id.mapped('servicios'))

    @api.depends("invoice_sheet_id")
    def _compute_exportaciones(self):
        for rec in self:
            rec['exportaciones']= sum(rec.invoice_sheet_id.mapped('exportaciones'))

    @api.depends("invoice_sheet_id")
    def _compute_ventas(self):
        for rec in self:
            rec['ventas']= sum(rec.invoice_sheet_id.mapped('ventas'))
            
    @api.depends("invoice_sheet_id")
    def _compute_invoice_iva(self):
        for rec in self:
            rec['iva']= sum(rec.invoice_sheet_id.mapped('iva'))