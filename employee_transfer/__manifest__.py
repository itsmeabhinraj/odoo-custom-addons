# -*- coding: utf-8 -*-\
{
    'name': 'Employee Transfer',
    'version': '1.2',
    'application': True,
    'category': 'hr',
    'installable': True,
    'auto_install': True,
    'depends': ['base','hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/employee_transfer.xml',
        'views/employee_transfer_menu.xml',
    ],
}
