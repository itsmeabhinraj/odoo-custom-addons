from odoo import fields,models

class EstatePropertytype(models.Model):
    _name='estate.property.type'
    _description ="Estate property details"

    name_type=fields.Char('Property type name', required=True, translate=True)
