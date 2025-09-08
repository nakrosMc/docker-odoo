from odoo import models, fields, api, _

class HrLeaveMotive(models.Model):
    _name = 'hr.leave.motive'
    _description = 'Motivo de Ausencia'

    name = fields.Char(string='Motivo', required=True)
    active = fields.Boolean(string='Activo', default=True, help="Si no está activo, no se podrá seleccionar en nuevas ausencias.")

