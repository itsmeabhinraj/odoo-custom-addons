from odoo import api,fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_ids = fields.Many2many(string="Invoices",comodel_name='account.move',compute='_compute_invoices')
    invoice_count = fields.Integer(string="Invoice Count",compute='_compute_invoices')
    invoice_id = fields.Many2one('account.move')
    invoices = fields.Char()
    related_so_ids = fields.Many2many('account.move')
    #
    # @api.depends("order_line.move_ids", "related_so_ids")
    # def _compute_invoices(self):
    #     for order in self:
    #         # Fetch invoices from the sale order lines and related sale orders
    #         invoices = order.order_line.move_ids.filtered(
    #             lambda r: r.move_type in ("out_invoice", "out_refund"))
    #         related_invoices = order.related_so_ids.mapped("invoice_ids")
    #
    #         # Combine invoices from the current SO and its related SOs
    #         order.invoice_ids = invoices | related_invoices
    #         order.invoice_count = len(order.invoice_ids)
    #
    #
    # def action_view_invoice(self):
    #     action = self.env.ref("account.action_move_out_invoice_type").read()[0]
    #     action["domain"] = [("id", "in", self.invoice_ids.ids)]
    #     return action

    # @api.depends('order_line.invoice_lines','invoice_ids')
    # def _get_invoiced(self):
    #     for move in self:
    #         related_invoices = self.env['account.move'].search([(self.id,'in',self.invoice_ids)])
    #                             # invoice_ids.related_so_ids.mapped("invoice_ids"))
    #         print('invoice',related_invoices)
    #         move.invoice_count = len(move.invoice_ids)
    #         print('invoice2',move.invoice_count)
    # @api.depends("related_so_ids")
    # def _compute_invoices(self):
    #     print('now',self)
    #     for record in self:
    #        # record.count_invoice = len(record.invoice_id)
    #        record.count_invoice = self.invoice_id.search(
    #            [("related_so_ids", '=', self.related_so_ids)])
    #        print(record.count_invoice)
    #        print("1001")

    @api.depends("order_line.invoice_lines", "related_so_ids")
    def _compute_invoices(self):
        for order in self:
            print('com imv',self)
            print(self.invoice_ids.id)
            # invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('out_invoice', 'out_refund'))
            # print(invoices)
            related_invoices = order.invoice_id.related_so_ids.mapped("invoice_ids")
            # Combine invoices from the current SO and its related SOs
            order.invoice_ids = related_invoices
            order.invoice_count = len(order.invoice_ids)

    def action_view_invoice(self):
       # '''invoice smart butn adding values'''
         return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'domain': [('related_so_ids', '=', self.id)],
            'context': "{'create':False}",
        }

    # def action_view_invoice(self):
    #     # invoices = self.mapped('invoice_ids')
    #     print(self)









        # self.ensure_one()
        # if self.invoice_id:
        #     return {
        #         'name': 'Invoice',
        #         'type': 'ir.actions.act_window',
        #         'view_mode': 'form',
        #         'res_model': 'account.move',
        #         'res_id': self.invoice_id.id,
        #         'domain':[('id', 'in', self.invoice_id.ids)],
        #         'context': {'create': False},
        #     }


        # invoices = self.mapped('invoice_ids')
        # print(invoices)
        # return {
        #     'name': 'Related invoices',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'list,form',
        #     'res_model': 'account.move',
        #     'domain': [('id', 'in',
        #                 (self.invoice_ids.related_so_ids.ids + invoices.ids))],
        #     'context': {'create': False},
        # }

        # action = super().action_view_invoice()
        # invoices = self.mapped('invoice_ids')
        # invoices2 = self.mapped('invoice_id.related_so_ids')
        # action['domain'] = [('id', 'in', invoices.ids)]
        # # print(self.invoice_ids.related_so_ids.ids)
        # return action
    #


 # # demo fleet
 # def _compute_count_invoice(self):
 #        for record in self:
 #            # record.count_invoice = len(record.invoice_id)
 #            record.count_invoice = (self.env['account.move'].
 #            search_count(
 #                [("auction_id", '=', self.id)]))
 #            print(record.count_invoice)
 #            print("1001")
 #
 #    def all_invoice_listed(self):
 #        '''invoice smart butn adding values'''
 #        return {
 #            'type': 'ir.actions.act_window',
 #            'name': 'Invoice',
 #            'view_mode': 'list',
 #            'res_model': 'account.move',
 #            'domain': [('auction_id', '=', self.id)],
 #            'context': "{'create':False}"
 #        }










