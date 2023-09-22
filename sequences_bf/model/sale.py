from odoo import models, fields, api

class sale_inherit(models.Model):
    _inherit='sale.order'

    operation_date = fields.Datetime(string = 'Fecha de Operacion')
    invoice_fel= fields.Char(string='Factura FEL')
    invoice_code = fields.Char(string='Referencia Interna')
    sequence = fields.Char(string='Correlativo Interno')

    def _prepare_invoice(self):
        invoice_vals = super(sale_inherit, self)._prepare_invoice()
        invoice_vals['invoice_date'] = self.operation_date
        invoice_vals['validation_code'] = self.invoice_fel
        invoice_vals['ref'] = self.invoice_code
        invoice_vals['invoice_code'] = self.sequence
        return invoice_vals
