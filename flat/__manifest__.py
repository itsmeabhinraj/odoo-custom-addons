# -*- coding: utf-8 -*-
{
    'name': 'Flat Managment',
    'version': '1.2',
    'category': 'sale',
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
    'depends':['base','sale_management'],
    'data': [
        'views/flat_management_views.xml',
        'views/flat_managment_menus.xml',
    ]
}