from odoo import fields,models

class PosConfigSettings(models.Model):

    _inherit = 'pos.config.settings'

    is_category_discount = fields.Boolean('Apply Category Wise Discount')
