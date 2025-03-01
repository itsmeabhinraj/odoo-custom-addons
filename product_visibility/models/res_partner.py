from odoo import fields, models
class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_product_ids = fields.Many2many('product.template',string='product')
    allowed_category_ids = fields.Many2many('product.public.category', string="Allowed Categories")
        # product = fields.Boolean(string="Product")