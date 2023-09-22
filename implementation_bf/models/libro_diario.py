# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class account_view_move_line(models.Model):

    _inherit='account.move.line'

    asiento = fields.Char(related='move_id.sequence', string="No. Asiento")
    comentario = fields.Char(related='move_id.comment', string="Comentario")