report- <odoo>
    <template id="report_fleet_auction_pdf">
        <t t-call="web.html_container">
            <t t-call="web.internal_layout">
                <div class="page">
                    <h2>Fleet Auction Report</h2>
                    <p><strong>From Date:</strong> <span t-esc="from_date"/></p>
                    <p><strong>To Date:</strong> <span t-esc="to_date"/></p>
                    <p><strong>State:</strong> <span t-esc="state"/></p>
                    <p><strong>Customer:</strong> <span t-esc="customer"/></p>
                    <p><strong>Responsible:</strong> <span t-esc="responsible"/></p>
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Customer Name</th>
                                <th>Bid Amount</th>
                                <th>State</th>
                                <th>Fleet Name</th>
                                <th>Current Asset Value</th>
                                <th>Won Amount</th>
                                <th>Bid Start Date</th>
                                <th>Bid End Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-foreach="results" t-as="result">
                                <tr>
                                    <td><span t-esc="result['customer_name']"/></td>
                                    <td><span t-esc="result['bid_amount']"/></td>
                                    <td><span t-esc="result['state']"/></td>
                                    <td><span t-esc="result['fleet_name']"/></td>
                                    <td><span t-esc="result['current_asset_value']"/></td>
                                    <td><span t-esc="result['won_amount']"/></td>
                                    <td><span t-esc="result['bid_start_date']"/></td>
                                    <td><span t-esc="result['bid_end_date']"/></td>
                                </tr>
                            </t>
                        </tbody>
                    </table>
                </div>
            </t>
        </t>
    </template>

#     <report id="report_fleet_auction_pdf"
#             string="Fleet Auction Report"
#             model="fleet.auction.wizard"
#             report_type="qweb-pdf"
#             name="your_module.report_fleet_auction_pdf"
#             file="your_module.report_fleet_auction_pdf"
#             paperformat="a3"/>
# </odoo>
# Another xml report -<odoo>
#     <record id="paperformat_a3" model="report.paperformat">
#         <field name="name">A3</field>
#         <field name="format">A3</field>
#         <field name="page_width">297</field>
#         <field name="page_height">420</field>
#         <field name="orientation">Portrait</field>
#         <field name="margin_top">10</field>
#         <field name="margin_bottom">10</field>
#         <field name="margin_left">10</field>
#         <field name="margin_right">10</field>
#         <field name="header_line">False</field>
#         <field name="header_spacing">0</field>
#         <field name="dpi">90</field>
#     </record>
# </odoo>










wizards- from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class FleetAuctionWizard(models.TransientModel):
    _name = 'fleet.auction.wizard'
    _description = 'Fleet Auction Report Wizard'

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string="State", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    responsible_id = fields.Many2one('res.users', string="Responsible")

    def action_generate_pdf(self):
        # Validate dates
        if self.from_date > self.to_date:
            raise UserError("From Date cannot be greater than To Date.")

        # Fetch data from the database
        query = """
            SELECT 
                c.name AS customer_name,
                f.bid_amount AS bid_amount,
                f.state AS state,
                f.fleet_name AS fleet_name,
                f.current_asset_value AS current_asset_value,
                f.won_amount AS won_amount,
                f.bid_start_date AS bid_start_date,
                f.bid_end_date AS bid_end_date
            FROM 
                fleet_auction f
            JOIN 
                res_partner c ON f.customer_id = c.id
            WHERE 
                f.bid_start_date >= %s AND f.bid_end_date <= %s
                AND f.state = %s
                AND (f.customer_id = %s OR %s IS NULL)
                AND (f.responsible_id = %s OR %s IS NULL)
        """
        self.env.cr.execute(query, (
            self.from_date, self.to_date, self.state,
            self.customer_id.id or None, self.customer_id.id or None,
            self.responsible_id.id or None, self.responsible_id.id or None
        ))
        results = self.env.cr.dictfetchall()

        # Check if data is available
        if not results:
            raise UserError("No data available to generate the report.")

        # Pass data to the PDF report
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'state': self.state,
            'customer': self.customer_id.name if self.customer_id else 'All',
            'responsible': self.responsible_id.name if self.responsible_id else 'All',
            'results': results,
        }
        return self.env.ref('your_module.report_fleet_auction_pdf').report_action(self, data=data)

wizard view =

report- <odoo>
    <template id="report_fleet_auction_pdf">
        <t t-call="web.html_container">
            <t t-call="web.internal_layout">
                <div class="page">
                    <h2>Fleet Auction Report</h2>
                    <p><strong>From Date:</strong> <span t-esc="from_date"/></p>
                    <p><strong>To Date:</strong> <span t-esc="to_date"/></p>
                    <p><strong>State:</strong> <span t-esc="state"/></p>
                    <p><strong>Customer:</strong> <span t-esc="customer"/></p>
                    <p><strong>Responsible:</strong> <span t-esc="responsible"/></p>
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Customer Name</th>
                                <th>Bid Amount</th>
                                <th>State</th>
                                <th>Fleet Name</th>
                                <th>Current Asset Value</th>
                                <th>Won Amount</th>
                                <th>Bid Start Date</th>
                                <th>Bid End Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-foreach="results" t-as="result">
                                <tr>
                                    <td><span t-esc="result['customer_name']"/></td>
                                    <td><span t-esc="result['bid_amount']"/></td>
                                    <td><span t-esc="result['state']"/></td>
                                    <td><span t-esc="result['fleet_name']"/></td>
                                    <td><span t-esc="result['current_asset_value']"/></td>
                                    <td><span t-esc="result['won_amount']"/></td>
                                    <td><span t-esc="result['bid_start_date']"/></td>
                                    <td><span t-esc="result['bid_end_date']"/></td>
                                </tr>
                            </t>
                        </tbody>
                    </table>
                </div>
            </t>
        </t>
    </template>

    <report id="report_fleet_auction_pdf"
            string="Fleet Auction Report"
            model="fleet.auction.wizard"
            report_type="qweb-pdf"
            name="your_module.report_fleet_auction_pdf"
            file="your_module.report_fleet_auction_pdf"
            paperformat="a3"/>
</odoo>
Another xml report -<odoo>
    <record id="paperformat_a3" model="report.paperformat">
        <field name="name">A3</field>
        <field name="format">A3</field>
        <field name="page_width">297</field>
        <field name="page_height">420</field>
        <field name="orientation">Portrait</field>
        <field name="margin_top">10</field>
        <field name="margin_bottom">10</field>
        <field name="margin_left">10</field>
        <field name="margin_right">10</field>
        <field name="header_line">False</field>
        <field name="header_spacing">0</field>
        <field name="dpi">90</field>
    </record>
</odoo>




from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetAuctionReportWizard(models.TransientModel):
    _name = 'fleet.auction.report.wizard'
    _description = 'Fleet Auction Report Wizard'

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('ongoing', 'Ongoing'), ('confirmed', 'Confirmed'), ('success', 'Success'), ('canceled', 'Canceled')],
        string="State",
    )
    customer_id = fields.Many2one('res.partner', string="Customer")
    responsible_id = fields.Many2one('hr.employee', string="Responsible")

    def action_print_report(self):
        # Validate date range
        if self.from_date > self.to_date:
            raise UserError("'From Date' must be earlier than 'To Date'.")

        # Construct SQL query
        query = """SELECT
                select rp.name AS customer_name,
                fb.bid_price AS bid_amount,
                faa.fleet_auction_state AS state,
                fv.name AS fleet_name,
                fv.current_value AS current_asset_value,
                faa.won_price AS won_amount,
                faa.start_date AS bid_start_date,
                faa.end_date AS bid_end_date
from fleet_auction_auction faa
inner join fleet_bid fb ON fb.auction_id = faa.id
inner join res_partner rp ON faa.customer_id = rp.id
inner join fleet_vehicle fv ON faa.vehicle_name = fv.id
            WHERE
                faa.start_date >= %s AND faa.end_date <= %s
        """
        params = [self.from_date, self.to_date]

        if self.state:
            query += " AND faa.fleet_auction_state = %s"
            params.append(self.state)
        if self.customer_id:
            query += " AND rp.id = %s"
            params.append(self.customer_id.id)
        if self.responsible_id:
            query += " AND faa.responsible = %s"
            params.append(self.responsible_id.id)

        self.env.cr.execute(query, tuple(params))
        report_data = self.env.cr.dictfetchall()

        if not report_data:
            raise UserError("No data available for the selected criteria.")

        # Pass data to report
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'state': dict(self._fields['state'].selection).get(self.state),
            'customer': self.customer_id.name if self.customer_id else 'All',
            'responsible': self.responsible_id.name if self.responsible_id else 'All',
            'report_data': report_data,
        }

        return self.env.ref('your_module.fleet_auction_report_action').report_action(self, data=data)