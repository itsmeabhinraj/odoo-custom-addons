from email.policy import default

from odoo import api, fields, models, _


class EmployeeTransfer(models.Model):
    _name = 'employee.transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Transfer ref", readonly=True,
                       default=lambda self: _('New'))
    request_date = fields.Date("Date", required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    reason = fields.Char('Reason for transfer', required=True)
    logined_employee_id = fields.Many2one('res.users', string='Employee',
                                          default=lambda self: self.env.uid)

    current_company_id = fields.Many2one('res.company', store=True,
                                         copy=False, string="Current Company",
                                         readonly=True,
                                         default=lambda
                                             self: self.env.company.id)
    choosen_company_id = fields.Many2one('res.company', store=True,
                                         string='Transfer company',
                                         default=lambda
                                             self: self.env.company.id)
    transfer_state = fields.Selection(
        string="State", selection=[('draft', 'Draft'),
                                   ('submitted', 'Submitted'),
                                   ('approved', 'Approved'),
                                   ('refused', 'Refused'),
                                   ('canceled', 'Canceled')],
        default='draft', tracking=True)
    check_company_field = fields.Boolean(compute='_compute_status')
    active = fields.Boolean('Active',default=1)

    @api.model
    def create(self, vals_list):
        '''sequance generator for employee transfer'''

        vals_list['name'] = self.env['ir.sequence'].next_by_code(
            'employee.transfer')
        return super().create(vals_list)

    def submit_request(self):
        '''for employees side this func will work'''
        self.transfer_state = 'submitted'
        print("sub")

    def confirm_request(self):
        '''Admin can approve the request through this action'''
        # print('1',self)
        # custom_employee_data = self.employee_id.copy_data()[0]
        # print(custom_employee_data)
        # custom_employee_data.update({
        #     'company_id':self.choosen_company_id.id,
        # })
        # print('2',self)
        # new_employee = self.env['hr.employee'].create(custom_employee_data)
        # print('3',new_employee)
        self.transfer_state = 'approved'
        # self.write({'employee_id':new_employee})
        self.employee_id.company_id = self.choosen_company_id
        print('last',self)

        # custom_employee_data = self.env['hr.employee'].create()
        # self.env['hr'].create({'name':self.employee_id})

        # })

    # def action_approve(self):
    #     employee_data = self.employee_id.copy_data()[0]
    #     employee_data.update({
    #         'company_id': self.new_company_id.id,
    #         'active': True,
    #     })
    #     new_employee = self.env['hr.employee'].create(employee_data)
    #     self.employee_id.active = False
    #     self.transfer_state = 'approved'
    #     self.write({'employee_id': new_employee.id})

    def refuse_request(self):
        self.transfer_state = 'refused'
        print('ref')

    def cancel_request(self):
        self.transfer_state = 'canceled'
        print('Cancel')

    @api.depends('transfer_state')
    def _compute_status(self):
        if self.transfer_state in ('draft','submitted'):
            if self.env.user.has_group('hr.group_hr_user'):
                self.check_company_field = False
            elif self.env.user.has_group('base.group_user'):
                self.check_company_field = True
        else:
            self.check_company_field = False
