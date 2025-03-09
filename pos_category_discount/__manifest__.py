# -*- coding: utf-8 -*-\
{
    'name': 'Pos Category Discount Limit',
    'version': '18.0.0.0',
    'license': 'LGPL-3',
    'category': 'Point of Sale',
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base','sale_management','point_of_sale'],
    'data': [
        'views/pos_category_views.xml',
    ],
}
