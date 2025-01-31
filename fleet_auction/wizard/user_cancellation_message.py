from odoo import fields,models

class UserCancellationMessage(models.TransientModel):
    _name ='user.cancellation.message'


    auction_id = fields.Many2one('fleet.auction.auction')
    reason = fields.Text("Reason for cancelation",store=1)

    def function1(self):
        print(self)
        record = self.env['fleet.auction.auction'].search([('fleet_auction_state','!=','canceled')])
        if record:
            record.fleet_auction_state = 'canceled'

    def cancel(self):
        print('cancel')
        return {'type': 'ir.actions.act_window_close'}

