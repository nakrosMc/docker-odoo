{
    'name': 'Promotional Sales',
    'version': '1.0',
    'category': 'Sale',
    'summary': 'Descuento de ventas por temporada.',
    'depends': ['sale'],
    'data': [
        'data/promo_campaign_data.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}