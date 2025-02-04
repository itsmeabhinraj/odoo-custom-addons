# -*- coding: utf-8 -*-
'''FLeet auction module handles the auction of the vehicles and the customer bid
y'''
from odoo import api, Command, fields, models, _
# from odoo.api import readonly
from odoo.exceptions import ValidationError, UserError


class FleetAuctionAuction(models.Model):
    '''Fleet auction class'''
    _name = 'fleet.auction.auction'
    _description = 'Fleet Auction Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Fleet Reference", readonly=True,
                       default=lambda self: _('New'))
    vehicle_name = fields.Many2one("fleet.vehicle",
                                   required=True, copy=False)
    brand = fields.Char('Brand')
    start_date = fields.Date("Start date",required=True)
    end_date = fields.Date("End date",required=True)
    active = fields.Boolean('Active', default=1)
    fleet_auction_state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('ongoing', 'Ongoing'),
                   ('confirmed', 'Confirmed'),
                   ('success', 'Success'),
                   ('canceled', 'Canceled')],
        default='draft'
    )
    # image = fields.Image("Image")
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False, string="Company",readonly=True,
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda
                                      self: self.env.company.currency_id.id)
    start_price = fields.Monetary('Start price', copy=False,required=True)
    won_price = fields.Monetary('Won price', copy=False)
    responsible_id = fields.Many2one('res.users', required=True,
                                     readonly=True,
                                  string="Responsible",
                                  default=lambda self: self.env.uid)
    description = fields.Html("vehicle description")
    customer_id = fields.Many2one("res.partner", string="Customer")
    # customer_id=fields.Many2one("fleet.bid",String="Customer")
    customer_phone = fields.Char(related='customer_id.phone')
    customer_email = fields.Char(related='customer_id.email')
    street = fields.Char(related='customer_id.street',)
    street2 = fields.Char(related='customer_id.street2',)
    city = fields.Char(related='customer_id.city')
    state_id = fields.Many2one(related='customer_id.state_id')
    zip = fields.Char(related='customer_id.zip')
    country_id = fields.Many2one(related='customer_id.country_id')

    bid_ids = fields.One2many("fleet.bid", "auction_id")
    confirm_bid_ids = fields.One2many("fleet.bid",
                                       "auction_id",
                                      compute="_compute_confirm_bids")
    best_bid = fields.Float(string="bid")
    same_bid = fields.Char(string="Auction_bid")
    tag_ids = fields.Many2many("crm.tag", string="Tag")
    bid_count = fields.Integer('count', compute="_compute_bid_count",
                               default=0)

    expense_ids = fields.One2many("fleet.expense",
                                  'auction_id')
    expense_id = fields.Many2one('fleet.expense')
    total_expense = fields.Monetary("Expenses",
                                    compute="_compute_total_expense")

    invoice_id = fields.Many2one('account.move')
    status_invoice = fields.Selection(related='invoice_id.status_in_payment')
    count_invoice = fields.Integer('Invoice', compute="_compute_count_invoice")
    # cancel_id = fields.One2many('user.cancellation.message','auction_id')

    @api.model
    def create(self, vals_list):
        """Sequance code are created here.name is the sequance field name """
        vals_list['name'] = self.env['ir.sequence'].next_by_code(
            'fleet.auction')
        print("sa",vals_list)
        return super().create(vals_list)

    @api.model
    @api.constrains('start_date', 'end_date')
    def date_constrains(self):
        """applying validation for start_date of auction and end_date.If the
    selected date end_date is before the start_date a error popup apprears"""
        for records in self:
            if records.start_date > records.end_date:
                raise ValidationError(_("Date should be apply before end"))

    def auction_cancel(self):
        """while Cancel auction button triggered state changes to canceled"""
        if self.fleet_auction_state == 'success':
            raise UserError('An error occured,Already auction success')
        elif self.env.user.has_group('fleet_auction.group_fleet_manager'):
            self.fleet_auction_state = 'canceled'
        else:
            print('user spotted')
            # self.ensure_one()
            return {'type': 'ir.actions.act_window',
                    'name': _('Cancellation Message'),
                    'res_model': 'user.cancellation.message',
                    'target': 'new',
                    'view_mode': 'form',
                    'context': {'default_res_id': self.id}}

    def auction_end(self):
        """while End Auction button triggered state changed to success"""
        if self.bid_ids:
            self.fleet_auction_state = 'success'
            sorted_value = self.bid_ids.sorted(lambda a: a.bid_price, reverse=True)
            print(sorted_value)
            self.won_price = sorted_value[0].bid_price
            self.customer_id = sorted_value[0].bid_customer_id
        else:
            raise UserError("Please add a bid")

    def auction_confirm(self):
        """While Confirm button triggered state changes to Confirmed"""
        for records in self:
            if records.start_price <= 0:
                raise ValidationError(_("Enter a price here"))
        if self.fleet_auction_state == 'canceled':
            raise UserError("Error--- already canceled")
        self.fleet_auction_state = 'confirmed'

    def auction_reset(self):
        """while Reset button triggerd state chnage back to draft form"""
        self.fleet_auction_state = 'draft'

    def create_invoice(self):
        """invoice for the vehicle auction and their expenses are arranged here.
        vehicle and expense added as description(name) so expense record seperatly
        added using command.create and the stored list called in invoice line ids using + icon.
        self.invoice_id - assinging the values of invoice data into record - invoice_id many 2 one field we created above.
        so the account.move get data from here.self is for record data store"""
        expense_record = [
            Command.create({
                'name': record.name,
                'price_unit': record.expense_amount, }) for record in
            self.expense_ids
        ]
        self.invoice_id = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'partner_id': self.customer_id.id,
            'currency_id': self.currency_id.id,
            'auction_id': self.id,
            'invoice_line_ids': [
                Command.create({'name': self.vehicle_name.name,
                                'price_unit': self.won_price,
                                })] + expense_record,
        }])
        # invoice.invoice_ids.action_post()
        # self.fleet_auction_state = 'invoiced'

    # best_value = self.confirm_bid_ids
    @api.depends('bid_ids.states')
    def _compute_confirm_bids(self):
        """computing the confirmed state bid based on conditons and stores in
        a one 2 many field"""
        for record in self:
            record.confirm_bid_ids = record.bid_ids.filtered(
                lambda best_value: best_value.states == "confirmed")

    def _compute_bid_count(self):
        '''computing the count of bids.here i added total count bid_ids'''
        for record in self:
            record.bid_count = len(record.bid_ids)
            print(record.bid_count)

    def total_bid_count_action(self):
        '''bid smart button action name .viewing of smart tab'''
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bids',
            'view_mode': 'list',
            'res_model': 'fleet.bid',
            'domain': [('auction_id', '=', self.id)],
            'context': "{'create': False}"
        }

    # @api.depends(invoice_id)
    def _compute_count_invoice(self):
        for record in self:
            # record.count_invoice = len(record.invoice_id)
            record.count_invoice = (self.env['account.move'].
            search_count(
                [("auction_id", '=', self.id)]))
            print(record.count_invoice)
            print("1001")

    def all_invoice_listed(self):
        '''invoice smart butn adding values'''
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('auction_id', '=', self.id)],
            'context': "{'create':False}"
        }

    @api.depends('expense_ids.expense_amount')
    def _compute_total_expense(self):
        """computing the totat expenses in the . each auction"""
        for record in self:
            record.total_expense = sum(line.expense_amount for
                                       line in record.expense_ids)

    def create_auction_auto(self):
        '''function for the auto scheduled action to start the auction on
        start date amd end in end date automatically based on date '''
        print(self)
        today = fields.Date.today()
        actions = self.search(
            [('fleet_auction_state', 'in', ['draft', 'confirmed'])])
        # ,('start_date','<=','today'))])
        # ('start_date','<=','today'),('end_date','>=','today'))])
        print(actions)
        for values in actions:
            print(values.start_date)
            print(values.end_date)
            if (values.fleet_auction_state == 'draft' and
                    values.start_date <= today):
                values.fleet_auction_state = 'confirmed'
            elif (values.fleet_auction_state == 'confirmed' and
                  values.end_date < today):
                values.fleet_auction_state = 'success'
                values.send_confirmation()

    def send_confirmation(self):
        '''confirmation mail sending through function'''
        for auction in self:
            template = self.env.ref('fleet_auction.confirmation_mail_template')
            template.send_mail(auction.id, force_send=True)
            # print(auction)

