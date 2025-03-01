from odoo import fields,models

class ResPartner(models.Model):
    '''inheriting model res.user to add a allowed product field'''
    _inherit = 'res.partner'

    allowed_products_ids = fields.Many2many('product.template',string="Allowed products")
    allowed_category_ids = fields.Many2many('product.category')
    # demo_field = fields.Boolean('Boolean')