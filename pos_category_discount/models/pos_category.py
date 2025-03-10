from odoo import fields, models

class PosCategory(models.Model):

    _inherit = 'pos.category'

    discount_type = fields.Selection(
        selection=[
            ('percentage', "Percentage"),
            ('fixed', "Fixed Price"),
        ],
        index=True, default='fixed')
    fixed_discount = fields.Float(string="Fixed Price", digits='Product Price')
    percent_discount = fields.Float(string="Percentage Discount")
