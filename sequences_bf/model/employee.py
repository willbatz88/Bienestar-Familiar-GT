from odoo import models, fields, api
class employee_inherit(models.Model):
    _inherit='hr.employee'

    sequence = fields.Char(string="Código", tracking=True)

    @api.model_create_multi
    def create(self, vals):
         for rec in vals:
             rec['sequence'] = self.env['ir.sequence'].next_by_code('employee_sequence')
         return super(employee_inherit, self).create(vals)
    
    def name_get(self):
        result = []
        for rec in self:
            name = '[' + str(rec.sequence) + ']' + ' - ' + rec.name
            result.append((rec.id, name))
        return result