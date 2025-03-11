# -*- coding: utf-8 -*-
from odoo import api,fields, models

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

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['discount_type','fixed_discount','percent_discount']
        return data
