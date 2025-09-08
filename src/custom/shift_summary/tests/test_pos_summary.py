from odoo.tests import TransactionCase, tagged
from datetime import datetime, timedelta

@tagged('post_install', '-at_install', 'point_test')
class TestShiftSummary(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.PosSession = self.env['pos.session']
        self.PosOrder = self.env['pos.order']
        self.PosOrderLine = self.env['pos.order.line']
        self.Product = self.env['product.product']

        # Crear producto de prueba
        self.product = self.Product.create({
            'name': 'Producto Test',
            'list_price': 10.0,
        })

        # Crear un partner de prueba
        self.partner = self.env['res.partner'].create({
            'name': 'Cliente Test',
        })

        # Buscar o crear una config de POS
        config = self.env['pos.config'].search([], limit=1)
        if not config:
            config = self.env['pos.config'].create({
                'name': 'POS Test Config',
                'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
            })

        # Crear una sesión POS
        self.session = self.PosSession.create({
            'user_id': self.env.uid,
            'config_id': config.id,
        })

        # Forzar tiempos de inicio y fin
        self.session.start_at = datetime.now() - timedelta(hours=2)
        self.session.stop_at = datetime.now()

        # Crear una orden vinculada a la sesión
        self.order = self.PosOrder.create({
            'session_id': self.session.id,
            'pricelist_id': config.pricelist_id.id,
            'partner_id': self.partner.id,
            'amount_total': 0.0,
            'amount_tax': 0.0,
            'amount_paid': 0.0,
            'amount_return': 0.0,
        })

        # Crear línea de orden
        self.PosOrderLine.create({
            'order_id': self.order.id,
            'product_id': self.product.id,
            'qty': 2,
            'price_unit': 10.0,
            'price_subtotal': 20.0,
            'price_subtotal_incl': 20.0,
        })

        # Simular los totales (en Odoo 17 no se recalculan con _amount_all)
        self.order.amount_total = 20.0
        self.order.amount_tax = 0.0
        self.order.amount_paid = 20.0
        self.order.amount_return = 0.0

    def test_compute_summary(self):
        """Debe calcular ventas, productos y tiempo activo"""
        self.session._compute_session_summary()

        self.assertEqual(
            self.session.summary_total_sales,
            20.0,
            "El total de ventas no es correcto."
        )
        self.assertIn(
            "Producto Test",
            self.session.summary_top_products,
            "El producto vendido no aparece en el resumen."
        )
        self.assertIn(
            "horas",
            self.session.summary_active_time,
            "El tiempo activo no se calculó correctamente."
        )

    def test_report_generation(self):
        """Debe generar el PDF del resumen sin errores"""
        
        report_action = self.env.ref('shift_summary.action_report_pos_session_summary')
        self.assertTrue(report_action, "No se encontró la acción del reporte.")
        
        pdf_content = self.env['ir.actions.report']._render_qweb_pdf(report_action, [self.session.id])
        
        self.assertTrue(pdf_content, "El reporte PDF no se generó correctamente.")
        self.assertTrue(pdf_content[0], "El reporte PDF no contiene datos.")