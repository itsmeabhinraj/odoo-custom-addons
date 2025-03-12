# -*- coding: utf-8 -*-
'''Adding new fields for discount in pos category'''
from odoo import api,fields, models

class PosCategory(models.Model):
    '''Adding new discount limit fields in this module'''

    _inherit = 'pos.category'

    discount_type = fields.Selection(
        selection=[
            ('none','None'),
            ('percentage', "Percentage"),
            ('fixed', "Fixed Price"),
        ],
        default='none')
    fixed_discount = fields.Float(string="Fixed Price", digits='Product Price')
    percent_discount = fields.Float(string="Percentage Discount")
    categ_limit_id = fields.Many2one("pos.conf")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Loading newly added fields into the pos """
        data = super()._load_pos_data_fields(config_id)
        data += ['discount_type','fixed_discount','percent_discount']
        return data
