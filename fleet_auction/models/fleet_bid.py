# -*- coding: utf-8 -*-
"""in module fleet auction , cutomer bids are manaeged in this model"""
from odoo import fields, models, _, api

class FleetBid(models.Model):
    """model created for the customer bid"""
    _name = 'fleet.bid'
    _description = "fleet auction bid start here"
    _rec_name = 'auction_id'

    bid_id = fields.Char(string="Bid ref", readonly=True,default=lambda self: _('New Bid'))
    auction_id = fields.Many2one('fleet.auction.auction',required=True,copy=False,ondelete='cascade')
    bid_amount = fields.Monetary(related='auction_id.start_price',readonly='True')
    bid_price = fields.Monetary('Bid Price')
    bid_date = fields.Date('Bid Date')
    phone = fields.Char('Phone')
    states = fields.Selection(string='States',selection=[('draft', 'Draft'), ('confirmed', 'Confirmed')],
                              default='draft')
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    bid_customer_id = fields.Many2one("res.partner", string="Customer")
    user_id = fields.Many2one('res.users',string="Responsible",readonly=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', copy=False, string="Company",
                                 readonly=True,default=lambda self: self.env.company.id)
    fleet_auction_state= fields.Selection(related='auction_id.fleet_auction_state')

    @api.model
    def create(self, vals_list):
        """creating the unique sequance num for bids generated"""
        vals_list['bid_id'] = self.env['ir.sequence'].next_by_code('bid.seq')
        return super().create(vals_list)

    def bid_confirm(self):
        """While Confirm button triggered state changes to Confirmed"""
        self.states = 'confirmed'
