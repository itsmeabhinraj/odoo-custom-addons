# -*- coding: utf-8 -*-
from odoo import api,fields,models

class PosConfigSettings(models.Model):

    _inherit = 'pos.config.settings'

    is_category_discount = fields.Boolean('Apply Category Wise Discount')

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['is_category_discount']
        return data
