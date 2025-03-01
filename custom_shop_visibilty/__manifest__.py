# -*- coding: utf-8 -*-\
{
    'name': 'Product visibilty',
    'version': '1.2',
    'category': 'shop',
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base','website_sale','website','sale_management'],
    'data': [
        'views/res_partner_view.xml',
    ],
}
