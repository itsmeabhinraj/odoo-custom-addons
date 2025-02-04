# -*- coding: utf-8 -*-
'''expense module-added corresponding fields here.total expense computed in
 main module'''
""""""
from odoo import fields, models


class FleetExpense(models.Model):
    _name = 'fleet.expense'
    _description = 'fleet auction expenses listed here'

    name = fields.Char("Description", required=True)
    expense_amount = fields.Monetary("Amount", copy=False, required=True)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    auction_id = fields.Many2one('fleet.auction.auction', required=True,
                                 copy=False, readonly=True, ondelete='cascade')
