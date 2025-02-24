from odoo import fields,models

class EstatePropertytag(models.Model):
    _name='estate.property.tag'
    _description ="Estate property tag listed"

    name=fields.Char('Property tage name', required=True)














