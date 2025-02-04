from odoo import fields,models
class FleetAuctionReport(models.TransientModel):
    _name = 'fleet.auction.report'

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('ongoing', 'Ongoing'),
                   ('confirmed', 'Confirmed'),
                   ('success', 'Success'),
                   ('canceled', 'Canceled')]
    )
    customer_id = fields.Many2one('res.partner','Customer')
    responsible_id = fields.Many2one('res.users',string="Responsible")

    def generate_pdf_report(self):
    #     #  demo file
        query = """select fb.bid_customer_id,fb.bid_price,fa.vehicle_name,
        fa.fleet_auction_state,fa.start_price,fa.best_bid,fa.start_date,
        fa.end_date from fleet_auction_auction as fa inner join fleet_bid as fb on 
        fb.auction_id=fa.id """
        if self.from_date:
            query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, self.to_date
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'date': self.read()[0], 'report': report}
        return self.env.ref('fleet_auction.action_report_fleet_auction_report').report_action(
            None, data=data)
        print("luca",self)



    def cancel(self):
        print('cancel')
        return {'type': 'ir.actions.act_window_close'}