from odoo import fields,models

class Flat(models.Model):
    _name = 'flat'
    _description = 'flat managemnt module'

    flat_id = fields.Many2one('flat.management', string='flats ordered')
    name = fields.Char('Flat', required=True)
    flat_description = fields.Text('Description')
    flat_amount = fields.Float('Price', copy=False, required=True)
