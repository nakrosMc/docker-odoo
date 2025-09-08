{
    'name': 'POS Session Summary Report',
    'version': '1.0',
    'summary': 'Genera un resumen automático del turno del cajero al cerrar la sesión del TPV.',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        'reports/report_pos_session_summary.xml',
        'reports/template_pos_session_summary.xml',
        'views/pos_session_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}