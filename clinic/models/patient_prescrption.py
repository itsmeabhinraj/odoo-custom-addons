from odoo import fields, models, api

class PatientOp(models.Model):
    _name='patient.prescription'
    _description ="patient diagnoisis details"

    med_name = fields.Char('Medicine')
    dosage = fields.Char('Dosage')
    total_qty = fields.Integer("Qty")
    serial_nos = fields.Many2one('patient.op', required=True, translatge=True)


