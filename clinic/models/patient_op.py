from odoo import fields, models, api


class PatientOp(models.Model):
    _name='patient.op'
    _description ="patient op details"
    _rec_name = 'name'

    # serial_no = fields.Integer('Serial no.', required=True, translatge=True)
    patient_id = fields.Many2one('res.partner',required=True,string='Patient name')
    age = fields.Integer(related='patient_id.age')
    gender = fields.Selection(related='patient_id.gender')
    token_no = fields.Integer("Token no")
    doctor_name = fields.Many2one('hr.employee',required=True)

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    doctor_fee = fields.Monetary(related='doctor_name.hourly_cost',string='Fee')

    # number = fields.Char('Serial num',readonly=True, tracking=True,
    #                      copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('patient.op'))

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('number', _('New')) == _('New'):
    #             vals['number'] = (self.env['ir.sequence'].next_by_code('patient.patient'))
    #     return super().create(vals_list)
    name = fields.Char(
        'Reference', default=lambda self: _('New'),
        copy=False, readonly=True, required=True)
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase.requisition.purchase.template')
        return super(PatientOp, self).create(vals)
