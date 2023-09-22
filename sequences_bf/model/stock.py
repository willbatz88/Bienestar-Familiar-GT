from odoo import models, fields, api, _
from odoo.exceptions import UserError
class stock_inherit(models.Model):
    _inherit='stock.warehouse'

    sequences = fields.Char(string="Código", tracking=True)

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec['sequences'] = self.env['ir.sequence'].next_by_code('store_sequence')
        return super(stock_inherit, self).create(vals)

    def write(self, vals):
        if not self.sequences:
            vals['sequences'] = self.env['ir.sequence'].next_by_code('store_sequence')
            return super(stock_inherit, self).write(vals)
    
    def name_get(self):
        result = []
        for rec in self:
            name = '[' + str(rec.sequences) + ']' + ' - ' + rec.name
            result.append((rec.id, name))
        return result