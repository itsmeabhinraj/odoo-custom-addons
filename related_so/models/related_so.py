from email.policy import default

from cffi.model import qualify
from lxml.html import find_rel_links

from odoo import api, fields, models, Command

class AccountMove(models.Model):
    '''inheriting the invoice here and add additional field related so.
    when the customer doing the invoice, they can add their to 'invoice' stage
    orders sale order lines to single invoice line '''

    _inherit = 'account.move'

    related_so_ids = fields.Many2many('sale.order',string='Related SO')
    so_invoiced_count = fields.Integer('Count',default=0)
    sale_name = fields.Char('sale ref')
    find_rel_sale_order = fields.Integer(compute='_compute_origin_so_count',string='relate so count')



    @api.depends('line_ids.sale_line_ids','related_so_ids')
    def _compute_origin_so_count(self):
        for move in self:
            move.sale_order_count = len(move.line_ids.sale_line_ids.order_id) + len(move.related_so_ids.order_line)
            print('salecount',move.sale_order_count)


    @api.onchange('related_so_ids')
    def related_fuction(self):
        print(self)
        for sale_order in self.related_so_ids:
            print('sale order',sale_order)
            sale_order.write({'invoice_id': self.id})
            for order_line in sale_order.order_line:
                print('order_line',order_line)
                invoice_line_vals = {
                    'product_id':order_line.product_id.id,
                    'quantity':order_line.product_uom_qty,
                    'price_unit':order_line.price_unit,
                    'tax_ids':order_line.tax_id,
                    'price_subtotal':order_line.price_subtotal,
                }
                print('product',order_line.product_id.id)
                self.update({'invoice_line_ids': [Command.create(invoice_line_vals)]})

    def action_post(self):
        ''' status of the selected sale order changed to invoiced stage'''
        self.related_so_ids.invoice_status = 'invoiced'
        super().action_post()

    def button_draft(self):
        '''invoice status changes to to invoice when reset draft click'''
        self.related_so_ids.invoice_status = 'to invoice'
        super().button_draft()

    def demo(self):
        print('demo')
        print(self.find_sale_order)

    def action_view_source_sale_orders(self):
        '''viewing the sale order smart button.
        Merge normal sale order and related so into this smart btn through this
        function'''
        source_orders = self.line_ids.sale_line_ids.order_id
        print(source_orders)
        return {
            'name': 'Related Sales Orders',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'sale.order',
            'domain': [('id', 'in', (self.related_so_ids.ids + source_orders.ids))],
            'context': {'create': False},
        }
        # super().action_view_source_sale_orders()




        # print(self.price_subtotal.id)

        # @api.depends('related_so_ids')
        # def _compute_origin_so_count(self):
        #     for move in self:
        #         move.find_rel_sale_order = len(move.related_so_ids.order_line)
        #         print(move.find_rel_sale_order)
        #     super()._compute_origin_so_count()

        # so_invoiced_count = len(self.related_so_ids)
        #     print(so_invoiced_count)

        # def action_view_source_sale_orders(self):
        #     self.ensure_one()
        #     value = super().action_view_source_sale_orders()
        #     sale_orders = self.mapped('related_so_ids') or self.mapped(
        #         'invoice_line_ids.sale_line_ids.order_id')
        #     # value['domain'] = [('id', 'in', sale_orders.ids)]
        #     value.write({
        #         'view_mode': 'tree,form',
        #         'domain': [('id', 'in', sale_orders.ids + self.related_so_ids)],
        #         'res.model': 'sale.order'
        #     })
        #     return value
        #
        # def action_total_sale_order(self):
        #     so_invoiced_count = len(self.related_so_ids)
        #     print(so_invoiced_count)
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'name': 'Sales order',
        #         'view_mode': 'list,form',
        #         'res_model': 'sale.order',
        #         'domain': [('id', 'in', self.related_so_ids.ids),
        #                    ('invoice_status', '=', 'invoiced')],
        #         'context': "{'create':False}"
        #     }



        # func_value = super().action_view_source_sale_orders()
        # print('hey',func_value)
        # for record in self:
        #     one = [Command.create{
        #         'domain': [('id', 'in', record.related_so_ids.ids)],
        #     }]
        # return [Command.write({'domain': [('id', 'in', self.related_so_ids.ids)]})]
        # value1 = ({
        #     'type': 'ir.actions.act_window',
        #     'name': 'Sale order',
        #     'view_mode': 'list,form',
        #     'res_model': 'sale.order',
        #     'domain': [('id', 'in', self.related_so_ids.ids),
        #                ('invoice_status', '=', 'invoiced')],
        #     'context': "{'create':False}"
        # })
        # # super().action_view_source_sale_orders()
        # result.append(value1)
        # return value1, super().action_view_source_sale_orders()

        # self.ensure_one()
        # source_orders = self.related_so_ids.order_line
        # result = self.env['ir.actions.act_window']._for_xml_id(
        #     'sale.action_orders')
        # if len(source_orders) > 1:
        #     result['domain'] = [('id', 'in',  self.related_so_ids.ids)]
        # elif len(source_orders) == 1:
        #     result['views'] = [
        #         (self.env.ref('sale.view_order_form', False).id, 'form')]
        #     result['res_id'] = source_orders.id
        # else:
        #     result = {'type': 'ir.actions.act_window_close'}
        # return result
        # sale_order_count += find_rel_sale_order
        # super().action_view_source_sale_orders()
