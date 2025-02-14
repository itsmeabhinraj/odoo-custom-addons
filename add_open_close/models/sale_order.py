from odoo import api,fields,models
from odoo.addons.test_convert.tests.test_env import record


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    change_state = fields.Selection(string="Status", selection=[('open','Open'),('close','Close')], compute='_compute_addon_open',default='open')
    check_sale = fields.Boolean(string='Sale order check',compute='_compute_check_sale')
    # check_status = fields.Boolean(string='Sale order status',compute='_compute_addon_open')

    def _compute_check_sale(self):
        for order in self:
            if order.state == 'sale':
                check_sale = True
            else:
                check_sale = False

    # @api.depends('check_sale')
    # def _compute_addon_open(self):
    #     print("haloo")

    @api.depends('check_sale')
    def _compute_addon_open(self):
        for order in self:
            print('oi')
            print(order.delivery_status)
            if order.state == 'sale' and order.delivery_status == 'full':
                order.change_state = 'close'
            else:
                order.change_state = 'open'
        value = self.env.search([]).filtered().sorted()

