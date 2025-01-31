# -*- coding: utf-8 -*-
{
    'name': 'Related SO',
    'version': '1.2',
    'category': 'sale',
    # 'author': "Author Name",
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
    'depends':['base','sale_management'],
    'data': [
        'views/related_so_views.xml',
        # 'views/sale_order_view.xml',
    ]
}