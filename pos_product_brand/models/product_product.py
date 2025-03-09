# -*- coding: utf-8 -*-
"""For adding a product brand field for pos"""
from odoo import api,fields,models

class ProductProduct(models.Model):
    """inheriting product module for add a brand field"""

    _inherit = 'product.product'

    product_brand = fields.Char("Brand")

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['product_brand']
        return data