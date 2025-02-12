# -*- coding: utf-8 -*-
import io
import json
from datetime import datetime

import xlsxwriter
from setuptools.command.alias import alias

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
            if records.from_date > records.to_date:
                raise ValidationError(_("Date should be apply before end"))

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
        # else:
        #     data = {
        #         'form_data': self.read()[0],
        #         'state': dict(self.fields_get('state').get('state').get('selection')),
        #         'reports': reports
        #     }
        return reports

    def generate_pdf_report(self):
        reports = self.fetch_data_report()
        data = {
            'form_data': self.read()[0],
            'state': dict(self.fields_get('state').get('state').get('selection')),
            'reports': reports
        }
        return self.env.ref('fleet_auction.action_report_fleet_auction_pdf_report').report_action(self, data=data)

    def generate_xlsx_report(self):
        reports = self.fetch_data_report()
        # reports = data['reports']
        print('wizard report', reports)
        data = {
            'form_data': self.read()[0],
            'state_value': dict(self.fields_get('state').get('state').get('selection')),
            'reports': reports
        }
        print('wizard data', data)
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'fleet.auction.report.wizard',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Fleet Auction Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print('hai xlsx')
        # reports=data['reports']
        reports = self.fetch_data_report()
        form_data = data['form_data']
        from_date = form_data.get('from_date')
        to_date = form_data.get('to_date')
        if from_date:
            reports=[report for report in reports if report['start_date']>= from_date]
        if to_date:
            reports=[report for report in reports if report['end_date']<= to_date]
        state_selection = dict(self.fields_get('state').get('state').get('selection'))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('fleet')
        # cell_format = workbook.add_format(
        #     {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '30px'})
        cell_format = workbook.add_format({'align':'center','bold':True, 'font_size': '11px','font_color': '#FFFFFF',
                                           'bg_color': '#000000'})
        name_txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        number_format = workbook.add_format({'font_size': '10px', 'align': 'right'})
        date_format = workbook.add_format({'num_format': 'YYYY-MM-DD'})
        sheet.insert_image('B2','../Pictures/Apple-Logosu.png',{'x_scale':0.03,'y_scale':0.01})
        sheet.merge_range('B4:C4',self.env.company.name,txt)
        sheet.merge_range('B5:C5',self.env.company.street,txt)
        sheet.merge_range('D9:K10', 'FLEET AUCTION REPORT', head)
        # Adjusting column size
        sheet.set_column('D:D',20)
        sheet.set_column('E:E',12)
        sheet.set_column('F:F',25)
        sheet.set_column('G:G',15)
        sheet.set_column('H:H',15)
        sheet.set_column('I:I',12)
        sheet.set_column('J:J',12)
        sheet.set_column('K:K',12)
        row = 15
        col = 3
        # table heading
        sheet.write(row,col, 'Customer',cell_format)
        sheet.write(row,col + 1, 'Bid Amount',cell_format)
        sheet.write(row,col + 2, 'Vehicle Name',cell_format)
        sheet.write(row,col + 3, 'Current Value',cell_format)
        sheet.write(row,col + 4, 'Won Amount',cell_format)
        sheet.write(row,col + 5, 'Start Date',cell_format)
        sheet.write(row,col + 6, 'End Date',cell_format)
        sheet.write(row,col + 7, 'State',cell_format)
        row +=1
        # displaying table content through iteration
        for row, report in enumerate(reports, start=16):
            sheet.write(row,col, report['customer_name'], name_txt)
            sheet.write(row,col + 1, report['bid_amount'], number_format)
            sheet.write(row,col + 2, report['fleet_name'], txt)
            sheet.write(row,col + 3, report['current_asset_value'], number_format)
            if (report['won_amount'] == report['bid_amount']):
                sheet.write(row,col + 4, report['won_amount'], number_format)
            sheet.write_datetime(row,col + 5, fields.Date.to_date(report['start_date']), date_format)
            sheet.write_datetime(row,col + 6, fields.Date.to_date(report['end_date']), date_format)
            sheet.write(row,col + 7, state_selection.get(report['state']), txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    # cancelation button in wizard
    def action_cancel(self):
        '''report generating wizards cancel button function'''
        return {'type': 'ir.actions.act_window_close'}
