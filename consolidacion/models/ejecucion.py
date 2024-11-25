# ejecucion.py
from odoo import models, fields, api

class Ejecucion(models.Model):
    _name = 'consolidacion.ejecucion'
    _description = 'Modelo de Ejecucion para Consolidacion'
    nombre = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripcion')
    fecha_inicio = fields.Date(string='Fecha de Inicio')
    fecha_fin = fields.Date(string='Fecha de Fin')
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('proceso', 'En Proceso'),
        ('finalizado', 'Finalizado')
    ], string='Estado', default='borrador')
    def action_ejecucion(self):
        for record in self:
            if record.estado == 'borrador':
                record.estado = 'proceso'
            elif record.estado == 'proceso':
                record.estado = 'finalizado'
        return True