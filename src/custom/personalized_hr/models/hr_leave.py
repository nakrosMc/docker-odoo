# -*- coding: utf-8 -*-

from odoo import models, fields

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    motive_id = fields.Many2one('hr.leave.motive', string='Motivo de Ausencia', tracking=True, help="Seleccione el motivo específico de esta ausencia.")