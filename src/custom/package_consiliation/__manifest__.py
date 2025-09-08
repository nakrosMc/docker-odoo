{
    'name': 'Package Consiliation',
    'version': '1.0',
    'category': 'Inventory/Warehouse',
    'summary': 'Agrupa productos en paquetes según reglas de tipo de producto.',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/stock_picking_views.xml',
        'wizards/package_consolidation_wizard_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}