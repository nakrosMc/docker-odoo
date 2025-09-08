from odoo import models, fields, api
from collections import defaultdict

class PackageConsolidationWizard(models.TransientModel):
    _name = 'package.consolidation.wizard'
    _description = 'Asistente para Sugerir Paquetes'

    picking_id = fields.Many2one('stock.picking', readonly=True)
    line_ids = fields.One2many('package.consolidation.wizard.line', 'wizard_id', string="Paquetes Sugeridos")

    @api.model
    def default_get(self, fields_list):
        res = super(PackageConsolidationWizard, self).default_get(fields_list)
        if 'picking_id' in res:
            picking = self.env['stock.picking'].browse(res['picking_id'])
            lines_by_type = defaultdict(lambda: self.env['stock.move.line'])

            lines_to_pack = picking.move_line_ids.filtered(lambda ml: not ml.result_package_id and ml.state == 'assigned')

            for line in lines_to_pack:
                package_type = line.product_id.package_type or 'normal'
                lines_by_type[package_type] += line

            wizard_lines = []
            for package_type, lines in lines_by_type.items():
                wizard_lines.append((0, 0, {
                    'package_type': package_type,
                    'move_line_ids': [(6, 0, lines.ids)]
                }))
            res['line_ids'] = wizard_lines
        return res

    def action_apply_consolidation(self):
        self.ensure_one()
        for line in self.line_ids:
            if line.move_line_ids:
                self.picking_id._put_in_pack(line.move_line_ids)
        return {'type': 'ir.actions.act_window_close'}

class PackageConsolidationWizardLine(models.TransientModel):
    _name = 'package.consolidation.wizard.line'
    _description = 'Línea de Sugerencia de Paquete'

    wizard_id = fields.Many2one('package.consolidation.wizard', required=True, ondelete='cascade')
    package_type = fields.Selection([
        ('normal', 'Normal'), ('fragile', 'Frágil'),
        ('refrigerated', 'Refrigerado'), ('heavy', 'Pesado / Voluminoso')
    ], string="Tipo de Paquete", readonly=True)
    move_line_ids = fields.Many2many('stock.move.line', string="Productos")