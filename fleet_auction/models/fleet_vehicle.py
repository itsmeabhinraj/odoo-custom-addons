# -*- coding: utf-8 -*-
from odoo import fields,models

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    current_value = fields.Monetary("Current value",copy=False)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    def add_auction(self):
        print('NAME',self.name)
        value = {
        'vehicle_name':self.id,
        'start_price':self.current_value,
        }
        create_vals = [dict(value)]
        return self.env['fleet.auction.auction'].create(create_vals)
