from odoo import fields,models

class FlatManagement(models.Model):
    _inherit = 'sale.order'

    flat_ordered_ids = fields.One2many('flat','flat_id')



