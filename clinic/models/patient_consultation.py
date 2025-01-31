from lxml.html import find_rel_links

from odoo import fields, models, api


class PatientConsultation(models.Model):
    _name='patient.consultation'
    _description ="patient consult details"

    serial_no = fields.Many2one('patient.op', required=True, translatge=True)
    patient_id = fields.Many2one('res.partner',required=True,string='Patient name')

    patient_token=fields.Integer(related='serial_no.token_no',invisible=True)
    patient_name = fields.Many2one(related='serial_no.patient_id')
    age = fields.Integer(related='serial_no.age')
    gender = fields.Selection(related='patient_id.gender')
    blood_grp = fields.Selection(related='patient_id.blood_grp')
    patient_weight = fields.Integer("Weight")
    patient_spoe = fields.Integer("SPOE")
    patient_height = fields.Integer('Height')
    patient_bld_pres = fields.Integer("Blood pressre")

    prescription_ids = fields.One2many('patient.prescription',inverse_name='serial_nos')