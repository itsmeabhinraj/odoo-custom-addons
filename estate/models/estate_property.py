from email.policy import default

from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name='estate.property'
    _description ="Estate property details"

    name=fields.Char('Property name', required=True, translate=True)
    description=fields.Char('Description',translate=True)
    postcode=fields.Integer('Postcode',required=True)
    creation_date=fields.Date("Creation date")
    date_availability=fields.Date('date available',default=today()+relativedelta(months=3),required=True,copy=False)
    expected_price=fields.Float("Sale price",readonly=True,copy=False)
    selling_price=fields.Float("Sale price",readonly=True,copy=False)
    bedrooms=fields.Integer("Bed room",default=2)
    garbage=fields.Boolean("Grabage",default=00)
    garden=fields.Boolean("Garden",default=10)
    garden_orientation=fields.Selection(
        string='type',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')]
    )
    active=fields.Boolean("Active",default=10)
    state=fields.Selection(
        string='State',
        selection=[('new','New'),('offer_received','Offer received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        required=True,copy=False,default='new'
    )
    # Many2one fields
    property_type_id=fields.Many2one("estate.property.type", string="Property type")
    salesman=fields.Many2one("res.users", string='Salesman',default=lambda self: self.env.user)
    buyer=fields.Many2one("res.partner", string='Buyer', copy=False)
    tag1_ids=fields.Many2many('estate.property.tag', string='Tags')
    offer_ids=fields.One2many("estate.property.offer","property_id")
    # computation
    total_area=fields.Float('Total area',compute="_compute_total",readonly=True)
    living_area=fields.Float('Living area',required=True)
    garden_area=fields.Float('Garden area')
    best_price=fields.Float('Best price',compute="_compute_bestprice")
    
    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_bestprice(self):
        for record in self:
            record.best_price=max(record.offer_ids.mapped('price')) if record.offer_ids else 0
    # onchange
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation='north'
        else:
            self.garden_area=0
            self.garden_orientation=False

    def sold_property(self):
        if self.state=='canceled':
            raise UserError('Cant we sold')
        self.state='sold'
    def cancel_property(self):
        if self.state=='sold':
            raise UserError("an error occured ,property already canceled and cant be sold")
        self.state='canceled'

    _sql_constraints = [
        ('expected_price', 'CHECK(price >= 0)',
         'The  price of property should be positive.')
    ]