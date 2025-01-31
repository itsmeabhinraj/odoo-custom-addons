from odoo import fields, models, api


class ClinicPartner(models.Model):
    _inherit = 'res.partner'

    # gender=fields.Char("enter",required=True)
    age = fields.Integer("Age", readonly=True,
                         compute="_date_computation")  # call the computation function from here
    date_of_birth = fields.Date(string='Date of birth')
    current_date = fields.Date(
        default=fields.Date.context_today)  # to get todays date
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    )
    blood_grp = fields.Selection(
        string="Blood Group",
        selection=[('a+ve', 'A+ve'), ('a-ve', 'A-ve'), ('b+ve', 'B+ve'),
                   ('b-ve', 'B-ve'), ('ab+ve', 'AB+ve'), ('ab-ve', 'AB-ve'),
                   ('o+ve', 'O+ve'), ('o-ve', 'O-ve'), ]
    )
    patient_id_num = fields.Integer(string='Patient ID')

    @api.depends("date_of_birth")
    def _date_computation(self):
        for record in self:
            if record.date_of_birth:
                today = record.current_date
                dob = record.date_of_birth
                record.age = today.year - dob.year - (
                            (today.month, today.day) < (dob.month, dob.day))
            else:
                record.age = 0

    _sql_constraints = [
        ('patient_id', 'unique(patient_id)',
         'The patient id must be unique.')
    ]
