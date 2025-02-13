# -*- coding: utf-8 -*-
'''This model generats both pdf and xlsx reports. Added two buttons for the report inside the wizard'''
import io
import json
import xlsxwriter
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import json_default
from datetime import datetime

class FleetAuctionReportWizard(models.TransientModel):
    '''Creating a wizard to display the report function. wizard through we can filter the data or all datas can be
    printed'''
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
    company_id = fields.Many2one('res.company',copy=False, string="Company", readonly=True,
                                 default=lambda self: self.env.company.id)

    @api.model
    @api.constrains('from_date', 'to_date')
    def date_constrains(self):
        '''validating entered dates'''
        for records in self:
            if records.from_date > records.to_date:
                raise ValidationError(_("Date should be apply before end"))

    def fetch_data_report(self):
        '''Fetching datas based our need from database using sql queries.And then apply comditions.Also
        filter data based on the data entered in wizard window'''
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
                  INNER JOIN fleet_vehicle fv ON faa.vehicle_name_id = fv.id
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
        else:
            return reports

    def action_generate_pdf_report(self):
        '''this functions calls through pdf button in wizard.then the data fetches from the query function
         (abstarct) and data passess the report '''
        reports = self.fetch_data_report()
        data = {
            'form_data': self.read()[0],
            'state': dict(self.fields_get('state').get('state').get('selection')),
            'reports': reports
        }
        return self.env.ref('fleet_auction.action_report_fleet_auction_pdf_report').report_action(self, data=data)

    def action_generate_xlsx_report(self):
        '''this function will works when the xlsx button clicked. Wizard data and record data are passed to the
        action manager.js and then controler to get the xlsx report. js will force to download the excel sheet'''
        reports = self.fetch_data_report()
        # use this - reports = data['reports']
        data = {
            'form_data': self.read()[0],
            'state_value': dict(self.fields_get('state').get('state').get('selection')),
            'reports': reports
        }
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
        '''function will automatically called through controler when we request xlsx report in xlsx button.'''
        reports=data['reports']
        # reports = self.fetch_data_report()
        # state_selection = dict(self.fields_get('state').get('state').get('selection'))
        state_selection = data['state_value']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('fleet')
        # applying text formats for different type datas
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '30px'})
        cell_format = workbook.add_format({'align':'center','bold':True, 'font_size': '11px','font_color': '#FFFFFF',
                                           'bg_color': '#000000'})
        name_txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        number_format = workbook.add_format({'font_size': '10px', 'align': 'right'})
        date_format = workbook.add_format({'num_format': 'YYYY-MM-DD'})
        # sheet data starts from here
        sheet.insert_image('I2','../Pictures/Apple-Logosu.png',{'x_scale':0.03,'y_scale':0.01})
        sheet.merge_range('I4:J4',self.env.company.name,txt)
        sheet.merge_range('I5:J5',self.env.company.street,txt)
        sheet.merge_range('A9:G10', 'FLEET AUCTION REPORT', head)
        # Adjusting column size
        sheet.set_column('A:A',20)
        sheet.set_column('B:B',12)
        sheet.set_column('C:C',25)
        sheet.set_column('D:D',15)
        sheet.set_column('E:E',15)
        sheet.set_column('F:F',12)
        sheet.set_column('G:G',12)
        sheet.set_column('H:H',12)
        row = 15
        col = 0
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

    def action_cancel(self):
        '''report generating wizards cancel button function'''
        return {'type': 'ir.actions.act_window_close'}
