from odoo import api, models, fields, _
from odoo.exceptions import UserError
class account_sequence_inherit(models.Model):
    _inherit='account.move'

    sequence = fields.Char(string="Código", tracking=True)
    invoice_code = fields.Char(string='Correlativo Interno', tracking=True)
    comment = fields.Char(string="Comentario")
    nit = fields.Char(related='partner_id.vat', string="NIT")

    codigo = fields.Selection([('1','Compras'), ('2','Servicios'), ('4','Pequeño Contribuyente')], string="Codigo de Documento")
    tipo_documento = fields.Selection([('fc','Factura'), ('fce','Factura Electronica'), ('fpq','Factura Pequeño Contribuyente'),('fe','Factura Especial')], string="Tipo de Documento")
    serie_factura = fields.Char('Serie de Factura')
    exento = fields.Monetary(string="Compra Generica")

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec['sequence'] = self.env['ir.sequence'].next_by_code('account_sequence')
        return super(account_sequence_inherit, self).create(vals)
    
    def create_purchase(self):
        for rec in self:
                purchase = self.env['invoice.purchase']
                new = purchase.create({
                    'fecha_documento': rec.invoice_date,
                    'no_factura': rec.ref,
                    'codigo': rec.codigo,
                    'tipo_documento': rec.tipo_documento,
                    'proveedor_id': rec.partner_id.id,
                    'serie_factura': rec.serie_factura,
                    'total': rec.tax_totals['amount_total'],
                    'compras_genericas': rec.exento
                })
                     

    def create_sale(self):
        for rec in self:
                sale = self.env['invoice.sale']
                new = sale.create({
                    'fecha_documento': rec.invoice_date,
                    'no_factura': rec.ref,
                    'codigo': rec.codigo,
                    #'tipo_documento': rec.tipo_documento,
                    'cliente_id': rec.partner_id.id,
                    'serie_factura': rec.serie_factura,
                    'total': rec.tax_totals['amount_total']
                })