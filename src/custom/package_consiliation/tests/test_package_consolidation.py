from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', 'package_tests')
class TestPackageConsolidation(TransactionCase):

    def setUp(self):
        super(TestPackageConsolidation, self).setUp()
        # Creamos productos con diferentes tipos de paquete
        self.product_normal = self.env['product.product'].create({
            'name': 'Producto Normal', 'package_type': 'normal'
        })
        self.product_fragile_A = self.env['product.product'].create({
            'name': 'Producto Frágil A', 'package_type': 'fragile'
        })
        self.product_fragile_B = self.env['product.product'].create({
            'name': 'Producto Frágil B', 'package_type': 'fragile'
        })

        # Creamos un albarán de salida
        self.picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
        })
        self.env['stock.move'].create([
            {'name': p.name, 'product_id': p.id, 'picking_id': self.picking.id, 'location_id': self.picking.location_id.id, 'location_dest_id': self.picking.location_dest_id.id, 'product_uom_qty': 1}
            for p in [self.product_normal, self.product_fragile_A, self.product_fragile_B]
        ])
        # Confirmamos y asignamos el stock
        self.picking.action_confirm()
        self.picking.action_assign()

    def test_01_consolidation_logic(self):
        """Prueba que el wizard sugiere y crea los paquetes correctamente."""
        # 1. Simulamos la apertura del wizard
        wizard_action = self.picking.action_suggest_packages()
        wizard = self.env['package.consolidation.wizard'].with_context(wizard_action['context']).create({})

        # Verificamos que el wizard proponga 2 paquetes
        self.assertEqual(len(wizard.line_ids), 2, "El wizard debería sugerir 2 paquetes.")

        # 2. Simulamos la aplicación de los paquetes
        wizard.action_apply_consolidation()

        # 3. Verificamos los resultados
        fragile_lines = self.picking.move_line_ids.filtered(lambda ml: ml.product_id.package_type == 'fragile')
        normal_line = self.picking.move_line_ids.filtered(lambda ml: ml.product_id.package_type == 'normal')

        # Contamos los paquetes únicos a través de las líneas de movimiento
        packages = self.picking.move_line_ids.mapped('result_package_id')
        self.assertEqual(len(packages), 2, "Se deberían haber creado 2 paquetes únicos.")

        # Los dos productos frágiles deben estar en el mismo paquete
        self.assertTrue(fragile_lines[0].result_package_id)
        self.assertEqual(fragile_lines[0].result_package_id, fragile_lines[1].result_package_id, "Los productos frágiles no están en el mismo paquete.")

        # El producto normal debe estar en un paquete diferente
        self.assertTrue(normal_line.result_package_id)
        self.assertNotEqual(normal_line.result_package_id, fragile_lines[0].result_package_id, "El paquete del producto normal debería ser diferente.")