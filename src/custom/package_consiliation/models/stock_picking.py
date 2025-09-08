from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_suggest_packages(self):
        # Este método abre el wizard y le pasa el albarán actual
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sugerir Paquetes',
            'res_model': 'package.consolidation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_picking_id': self.id}
        }