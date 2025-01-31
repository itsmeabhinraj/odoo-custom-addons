{
    'name': 'Clinic App',
    'version': '1.2',
    'application': True,
    'category': 'Medical',
    'depends': ['base','hr','hr_hourly_cost'],
    'data': [
        'security/ir.model.access.csv',
        'views/prescription_view.xml',
        'views/consultant_view.xml',
        'views/my_module_sequence.xml',
        'views/op_view.xml',
        'views/registration_view.xml',
        'views/clinic_menu.xml',
    ]
}