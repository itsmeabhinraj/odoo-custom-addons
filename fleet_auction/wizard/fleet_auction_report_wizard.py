from odoo import api,fields,models,_
from odoo.exceptions import ValidationError


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
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False, string="Company", readonly=True,
                                 default=lambda self: self.env.company.id)

    @api.model
    @api.constrains('from_date', 'to_date')
    def date_constrains(self):
        for records in self:
            print('welco')
            if records.from_date > records.to_date:
                raise ValidationError(_("Date should be apply before end"))

    def generate_pdf_report(self):
    #     #  demo file
        print('query')
        query = f"""SELECT rp.name AS customer_name,
                fb.bid_price AS bid_amount,
                faa.fleet_auction_state AS state,
                fv.name AS fleet_name,
                fv.current_value AS current_asset_value,
                faa.won_price AS won_amount,
                faa.start_date AS start_date,
                faa.end_date AS end_date
                FROM fleet_auction_auction faa
                INNER JOIN fleet_bid fb ON fb.auction_id = faa.id
                INNER JOIN res_partner rp ON faa.customer_id = rp.id
                INNER JOIN res_users rs ON faa.responsible_id = rs.id
                INNER JOIN res_company rc ON faa.company_id = rc.id
                INNER JOIN fleet_vehicle fv ON faa.vehicle_name = fv.id
             """

        if self.from_date:
            query += f""" WHERE faa.start_date >= '{self.from_date}' and faa.end_date <= '{self.to_date}'"""
        # self.env.cr.execute(query,(
        #     self.from_date,self.to_date
        # ))
        print('values')
        self.env.cr.execute(query)
        print('he')

        reports = self.env.cr.dictfetchall()

        print('report',reports)

        data = {
            'form_data': self.read()[0],
            'reports': reports
        }

        print(self.read()[0])
        print('data - ',data)

        return self.env.ref('fleet_auction.action_report_fleet_auction_report').report_action(self, data=data)

    def cancel(self):
        '''report generationg wizards cancel button'''
        return {'type': 'ir.actions.act_window_close'}