# -*- coding: utf-8

from odoo import fields, models
class GenerateBook(models.TransientModel):
    _name="generate.book.wizard"
    _description = "Generar Ventana de Libro Diario"

    date_begin = fields.Date(string="Fecha de Inicio", required=True)
    date_end = fields.Date(string="Fecha de Finalizacion", required=True)

    def action_print_report(self):
        domain = []
        date_begin = self.date_begin
        if date_begin:
            domain += [('date', '>=' , date_begin)]
        date_end = self.date_end
        if date_end:
            domain += [('date', '<=', date_end)]
        accounts = self.env['account.move.line'].search_read(domain, ['id', 'date', 'account_id', 'debit', 'credit', 'move_id', 'asiento', 'comentario', 'move_type'])
        data = {
            'accounts': accounts,
            'form_data': self.read()[0]
        }
        return self.env.ref('implementation_bf.report_libro_diario_xlsx').report_action(self, data=data)