from odoo import fields, models

class PosCategory(models.Model):

    _inherit = 'pos.category'

    discount_type = fields.Selection(
        selection=[
            ('percentage', "Percentage"),
            ('fixed', "Fixed Price"),
        ],
        help="Use the discount rules and activate the discount settings"
             " in order to show discount to customer.",
        index=True, default='fixed')
    fixed_discount = fields.Float(string="Fixed Price", digits='Product Price')
    percent_discount = fields.Float(string="Percentage Discount")
