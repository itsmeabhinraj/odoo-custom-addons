# -*- coding: utf-8 -*-
from odoo import fields, models


class FleetInvoice(models.Model):
    _inherit = 'account.move'

    auction_id = fields.Many2one('fleet.auction.auction')
    payment_status = fields.Selection(
        string='Paid status',
        selection=[('notpaid', 'Not Paid'),
                   ('paid', 'Paid')],
        default='notpaid', readonly=True
    )
    #
    # def action_post(self):
    #     super().action_post()
