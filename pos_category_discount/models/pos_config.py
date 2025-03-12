# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    """Extension of 'pos.config' for configuring pos category wise discount."""
    _inherit = 'pos.config'

    is_category_discount = fields.Boolean()

