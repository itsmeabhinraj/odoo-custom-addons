# -*- coding: utf-8 -*-
'''After an auction success, create a invoice for the customer who won the auction.'''
from odoo import fields, models

class FleetInvoice(models.Model):
    '''inheriting invoice module inside the fleet auction and directly linking  auction with invoice'''
    _inherit = 'account.move'

    auction_id = fields.Many2one('fleet.auction.auction',readonly=True)

