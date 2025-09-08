# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase, tagged
from odoo.fields import Date
from datetime import timedelta

@tagged('post_install', '-at_install', 'promotional_sales')
class TestProductPromotion(TransactionCase):

    def setUp(self):
        super(TestProductPromotion, self).setUp()
        self.ConfigParam = self.env['ir.config_parameter'].sudo()
        self.ProductTemplate = self.env['product.template']

        # Creamos productos de prueba
        self.promo_product = self.ProductTemplate.create({
            'name': 'Producto en Promoción',
            'list_price': 100.0,
            'is_special_promotion': True,
        })
        self.normal_product = self.ProductTemplate.create({
            'name': 'Producto Normal',
            'list_price': 200.0,
        })
    
    def _set_campaign_dates(self, start_delta, end_delta):
        """Función helper para configurar las fechas de la campaña."""
        today = Date.today()
        self.ConfigParam.set_param('promo_campaign.start_date', str(today + timedelta(days=start_delta)))
        self.ConfigParam.set_param('promo_campaign.end_date', str(today + timedelta(days=end_delta)))
        self.ConfigParam.set_param('promo_campaign.discount_percent', '20.0') # 20% de descuento para la prueba

    def test_01_apply_promotion(self):
        """Prueba que el precio se ajusta cuando la campaña está activa."""
        # Configuramos una campaña activa
        self._set_campaign_dates(start_delta=-1, end_delta=1)

        # Ejecutamos el script
        self.ProductTemplate._run_promo_price_update()

        # Refrescamos los valores de los productos desde la base de datos
        self.promo_product = self.promo_product.browse(self.promo_product.id)
        self.normal_product = self.normal_product.browse(self.normal_product.id)

        # Verificamos que el precio del producto en promoción se haya reducido un 20%
        self.assertAlmostEqual(self.promo_product.list_price, 80.0, "El precio de promoción no se aplicó correctamente.")
        self.assertEqual(self.promo_product.original_price, 100.0, "El precio original no se guardó.")
        
        # Verificamos que el precio del producto normal no haya cambiado
        self.assertEqual(self.normal_product.list_price, 200.0, "El precio del producto normal no debería haber cambiado.")

    def test_02_revert_promotion(self):
        """Prueba que el precio se revierte cuando la campaña termina."""
        # 1. Aplicamos la promoción primero
        self._set_campaign_dates(start_delta=-1, end_delta=1)
        self.ProductTemplate._run_promo_price_update()
        self.promo_product.browse(self.promo_product.id)
        self.assertAlmostEqual(self.promo_product.list_price, 80.0) # Confirmamos que se aplicó

        # 2. Ahora, configuramos una campaña que ya terminó
        self._set_campaign_dates(start_delta=-5, end_delta=-2)
        
        # 3. Ejecutamos el script de nuevo
        self.ProductTemplate._run_promo_price_update()
        self.promo_product.browse(self.promo_product.id)

        # Verificamos que el precio haya vuelto al original
        self.assertAlmostEqual(self.promo_product.list_price, 100.0, "El precio no se revirtió al original.")
        self.assertEqual(self.promo_product.original_price, 0.0, "El precio original no se limpió después de la campaña.")