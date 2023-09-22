from odoo import api, models, fields, _
from odoo.exceptions import UserError
class contact_inherit(models.Model):
    _inherit='res.partner'

    sequence = fields.Char(string="Código", default='Codigo', tracking=True)


    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if hasattr(rec, 'category_id'):
                for categorys in rec['category_id']:
                    category = self.env['res.partner.category'].browse(categorys[2][0])
                    if(category is not None):
                        if category.name == 'Cliente':
                            rec['sequence'] = self.env['ir.sequence'].next_by_code('client_sequence')
                        elif category.name == 'Proveedor':
                            rec['sequence'] = self.env['ir.sequence'].next_by_code('supplier_sequence')
            return super(contact_inherit, self).create(vals)
    
    def name_get(self):
        result = []
        for rec in self:
            if rec.sequence != False:
                 name = str(rec.sequence) + ' - ' + rec.name
                 result.append((rec.id, name))
        return result

        
                