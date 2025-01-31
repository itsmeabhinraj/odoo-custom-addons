# -*- coding: utf-8 -*-
{
    'name': 'Fleet Auction',
    'version': '1.2',
    'category': 'vehicle',
    # 'author': "Author Name",
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
    'depends':['base','hr','mail','contacts','fleet','crm','account'],
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/mail_confirmation_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_sequence_data.xml',
        'wizard/user_cancellation_view.xml',
        'views/fleet_invoice.xml',
        'views/fleet_expense_view.xml',
        'views/fleet_vehicle.xml',
        'views/fleet_bid_view.xml',
        'views/fleet_auction_view.xml',
        'views/fleet_auction_menu.xml',
    ]
}