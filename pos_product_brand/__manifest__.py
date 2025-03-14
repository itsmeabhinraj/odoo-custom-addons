# -*- coding: utf-8 -*-\
{
    'name': 'Pos Product Brand',
    'version': '18.0.0.0',
    'license': 'LGPL-3',
    'category': 'Point of Sale',
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base','sale_management','point_of_sale'],
    'data': [
        'views/product_product_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_brand/static/src/xml/orderline.xml',
            'pos_product_brand/static/src/js/pos_order_line.js',
        ],
    },
}
