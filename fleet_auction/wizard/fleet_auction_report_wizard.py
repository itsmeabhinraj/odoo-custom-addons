# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import json_default


class FleetAuctionReportWizard(models.TransientModel):
    _name = 'fleet.auction.report.wizard'


    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('ongoing', 'Ongoing'),
                   ('confirmed', 'Confirmed'),
                   ('success', 'Success'),
                   ('canceled', 'Canceled')])
    customer_id = fields.Many2one('res.partner', 'Customer')
    responsible_id = fields.Many2one('res.users', string="Responsible")
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
    #  safe code
    # def generate_pdf_report(self):
    #     '''pdf button in wizard which generate appropiate report based on the
    #     condition we given.'''
    #     query = f"""SELECT rp.name AS customer_name,
    #             fb.bid_customer_id AS bid_customer,
    #             fb.bid_price AS bid_amount,
    #             fb.user_id AS responsible_name,
    #             faa.fleet_auction_state AS state,
    #             fv.name AS fleet_name,
    #             faa.start_price AS current_asset_value,
    #             faa.start_date AS start_date,
    #             faa.end_date AS end_date,
    #             CASE WHEN faa.fleet_auction_state='success'
    #             THEN faa.won_price
    #             ELSE NULL END AS won_amount
    #             FROM fleet_auction_auction faa
    #             INNER JOIN fleet_bid fb ON fb.auction_id = faa.id
    #             INNER JOIN res_partner rp ON fb.bid_customer_id = rp.id
    #             INNER JOIN res_users rs ON faa.responsible_id = rs.id
    #             INNER JOIN res_company rc ON faa.company_id = rc.id
    #             INNER JOIN fleet_vehicle fv ON faa.vehicle_name = fv.id
    #          """
    #
    #     if self.from_date or self.to_date:
    #         query += f""" WHERE faa.start_date >= '{self.from_date}' and faa.end_date <= '{self.to_date}'"""
    #     if self.state:
    #         query += f"""AND faa.fleet_auction_state = '{self.state}'"""
    #     if self.customer_id:
    #         query += f"""AND rp.id = '{self.customer_id.id}'"""
    #     if self.responsible_id:
    #         query += f"""AND fb.user_id = '{self.responsible_id.id}'"""
    #
    #     self.env.cr.execute(query)
    #     reports = self.env.cr.dictfetchall()
    #
    #     print('report', reports)
    #     if reports:
    #         data = {
    #             'form_data': self.read()[0],
    #             'state': dict(self.fields_get('state').get('state').get('selection')),
    #             'reports': reports
    #         }
    #         return self.env.ref('fleet_auction.action_report_fleet_auction_report').report_action(self, data=data)
    #     else:
    #         raise UserError(_('No result found!'))


    def fetch_data_report(self):
        '''pdf button in wizard which generate appropiate report based on the
        condition we given.'''
        query = f"""SELECT rp.name AS customer_name,
                  fb.bid_customer_id AS bid_customer,
                  fb.bid_price AS bid_amount,
                  fb.user_id AS responsible_name,
                  faa.fleet_auction_state AS state,
                  fv.name AS fleet_name,
                  faa.start_price AS current_asset_value,
                  faa.start_date AS start_date,
                  faa.end_date AS end_date,
                  CASE WHEN faa.fleet_auction_state='success'
                  THEN faa.won_price
                  ELSE NULL END AS won_amount
                  FROM fleet_auction_auction faa
                  INNER JOIN fleet_bid fb ON fb.auction_id = faa.id
                  INNER JOIN res_partner rp ON fb.bid_customer_id = rp.id
                  INNER JOIN res_users rs ON faa.responsible_id = rs.id
                  INNER JOIN res_company rc ON faa.company_id = rc.id
                  INNER JOIN fleet_vehicle fv ON faa.vehicle_name = fv.id
               """

        if self.from_date or self.to_date:
            query += f""" WHERE faa.start_date >= '{self.from_date}' and faa.end_date <= '{self.to_date}'"""
        if self.state:
            query += f"""AND faa.fleet_auction_state = '{self.state}'"""
        if self.customer_id:
            query += f"""AND rp.id = '{self.customer_id.id}'"""
        if self.responsible_id:
            query += f"""AND fb.user_id = '{self.responsible_id.id}'"""

        self.env.cr.execute(query)
        reports = self.env.cr.dictfetchall()
        if not reports:
            raise UserError(_('No result found!'))
            # data = {
            #     'form_data': self.read()[0],
            #     'state': dict(self.fields_get('state').get('state').get('selection')),
            #     'reports': reports
            # }
        return reports

    def generate_pdf_report(self):
        reports = self.fetch_data_report()
        data = {
            'form_data': self.read()[0],
            'state': dict(self.fields_get('   state').get('state').get('selection')),
            'reports': reports
        }
        return self.env.ref('fleet_auction.action_report_fleet_auction_report').report_action(self, data=data)

    def generate_xls_report(self,response=None):
        data=self.fetch_data_report()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
        sheet.merge_range('A4:B4', 'Customer:', cell_format)
        sheet.merge_range('C4:D4', data['product'], txt)
        sheet.merge_range('A5:B5', 'Products', cell_format)
        for i, product in enumerate(data['products'],
                                    start=5):  # Start at row 6 for products
            sheet.merge_range(f'C{i}:D{i}', product, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


    def cancel(self):
        '''report generationg wizards cancel button'''
        return {'type': 'ir.actions.act_window_close'}
