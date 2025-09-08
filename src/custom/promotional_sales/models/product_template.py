from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_special_promotion = fields.Boolean(string="Promoción Especial", help="Marcar si este producto es parte de una campaña de promoción especial.")
    original_price = fields.Float(string="Precio Original", help="Precio del producto antes de aplicar el descuento de la promoción.", readonly=True, copy=False)
    
    @api.model
    def _run_promo_price_update(self):
        """
        Este método es llamado por la acción planificada.
        Aplica o revierte precios de promoción basado en las fechas de campaña.
        """
        # Obtenemos los parámetros de configuración del sistema
        config_params = self.env['ir.config_parameter'].sudo()
        start_date_str = config_params.get_param('promo_campaign.start_date')
        end_date_str = config_params.get_param('promo_campaign.end_date')
        discount_str = config_params.get_param('promo_campaign.discount_percent', '0.0')
        
        if not all([start_date_str, end_date_str, discount_str]):
            # Si no hay campaña configurada, no hacemos nada
            return
        
        today = fields.Date.context_today(self)
        start_date = fields.Date.from_string(start_date_str)
        end_date = fields.Date.from_string(end_date_str)
        discount_percent = float(discount_str)

        # Buscamos todos los productos marcados para la promoción
        promo_products = self.search([('is_special_promotion', '=', True)])

        if start_date <= today <= end_date:
            for product in promo_products:
                if not product.original_price:
                    product.original_price = product.list_price
                    
                discount_factor = 1 - (discount_percent / 100)
                product.list_price = product.original_price * discount_factor
        else:
            products_to_revert = promo_products.filtered(lambda p: p.original_price > 0)
            for product in products_to_revert:
                product.list_price = product.original_price
                product.original_price = 0.0

        return True