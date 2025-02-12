# -*- coding: utf-8 -*-
'''Creating a wizards to request user to enter reason for cancelation'''
from odoo import fields,models

class UserCancellationMessage(models.TransientModel):
    ''' wizard for auction cancelation'for the user'''
    _name ='user.cancellation.message'

    auction_id = fields.Many2one('fleet.auction.auction')
    reason = fields.Text("Reason for cancelation",store=1)

    def action_done(self):
        '''this button will cancel the auction'''
        record = self.env['fleet.auction.auction'].search([('fleet_auction_state','!=','canceled')])
        if record:
            record.fleet_auction_state = 'canceled'

    def action_cancel(self):
        """button for cancel the w"""
        return {'type': 'ir.actions.act_window_close'}

