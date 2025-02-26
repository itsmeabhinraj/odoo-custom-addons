
# -*- coding: utf-8 -*-\
{
    'name': 'Associated product',
    'version': '1.2',
    'application': True,
    'category': 'sales',
    'installable': True,
    'auto_install': False,
    'depends': ['base','sale_management'],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_views.xml',
        'views/sale_order_menu.xml',
    ],
}
