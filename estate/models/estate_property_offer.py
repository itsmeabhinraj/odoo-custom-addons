from datetime import timedelta
from email.policy import default

import dateutil
from dateutil.utils import today
from qrcode.util import create_data

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import date_utils


class EstatePropertyoffer(models.Model):
    _name='estate.property.offer'
    _description ="Estate property offers listed"

    price=fields.Float('Property price')
    status=fields.Selection(
        string='Status',
        selection=[('accepted','Accepted'),('refused','Refused')],
        copy=False
    )
    partner_id=fields.Many2one('res.partner',required=True)
    property_id=fields.Many2one('estate.property',required=True)
    # create_date=fields.Datetime.now('Created date')
    create_date = fields.Date(default=today(),string="Create Date")
    validity=fields.Integer("Validity",required=True,default=7)
    accepted_list=fields.Char()
    date_deadline=fields.Date("Date deadline",compute="_date_computation", inverse="_inverse_date")
    @api.depends("validity","create_date")
    def _date_computation(self):
        for record in self:
            record.date_deadline=fields.Date.add(today(),days=record.validity)
    def _inverse_date(self):
        for record in self:
            record.validity=(record.date_deadline-record.create_date).days

    def action_confirm(self):
        accepted_list=self.property_id.offer_ids.mapped('status')
        for record in accepted_list:
            if record=="accepted":
                raise UserError("Cant accept two or options same time")
        self.status='accepted'
        self.property_id.buyer=self.partner_id
        self.property_id.selling_price=self.price
    def action_refused(self):
        self.status='refused'
        self.property_id.selling_price=0

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)',
         'The price of the offer should be positive.')
    ]
