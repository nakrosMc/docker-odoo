from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    package_type = fields.Selection([
            ('normal', 'Normal'),
            ('fragile', 'Frágil'),
            ('refrigerated', 'Refrigerado'),
            ('heavy', 'Pesado / Voluminoso'),
        ], string="Tipo de Paquete", default='normal')