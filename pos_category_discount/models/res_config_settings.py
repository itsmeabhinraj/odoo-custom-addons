# -*- coding: utf-8 -*-
'''Adding field in pos settings'''
from odoo import api,fields,models

class ResConfigSettings(models.TransientModel):
    '''adding a new boolean field in pos settings for category wise discount '''

    _inherit = 'res.config.settings'

    is_category_discount = fields.Boolean(related='pos_config_id.is_category_discount',
                                          string='Apply Category Wise Discount',readonly=False)

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Loading newly added fields into the pos """
        data = super()._load_pos_data_fields(config_id)
        data += ['is_category_discount']
        return data
