# -*- coding: utf-8 -*-
"""Linking fleet vehicle module directly with fleet auction. So the auction can be created from fleet vehicle moule"""
from odoo import fields, models


class FleetVehicle(models.Model):
    """inheriting fleet vehicle module and add new button inside the module for auction.It works in the already
     existing module. Add a button,while button pass data of vehicle name and currect prize to the fleet auction module
      and a auction in draft state is created."""
    _inherit = 'fleet.vehicle'

    current_value = fields.Monetary("Current value", copy=False)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)

    def add_auction(self):
        '''function for the auction button'''
        value = {
            'vehicle_name': self.id,
            'start_price': self.current_value,
        }
        create_vehicle_auction = [value]
        return self.env['fleet.auction.auction'].create(create_vehicle_auction)
