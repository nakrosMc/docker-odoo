{
    'name': 'Control of Absences by Reason',
    'version': '1.0',
    'category': 'Human Resources/Time Off',
    'summary': 'Añade motivos personalizables a las ausencias y genera reportes.',
    'depends': ['hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_leave_views.xml',
        'views/hr_leave_report_views.xml',
        'views/hr_leave_motive_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}