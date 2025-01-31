from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    associated_products_ids = fields.Many2many('product.product',
                                               string='product')
    # associated_products_ids = fields.Many2many('product.template',string='product')
