# -*- coding: utf-8 -*-
from odoo import fields,models
from odoo.api import readonly


class FleetInvoice(models.Model):
    # _name = 'fleet.invoice'
    _inherit = 'account.move'

    auction_id = fields.Many2one('fleet.auction.auction')
    payment_status = fields.Selection(
        string='Paid status',
        selection=[('notpaid','Not Paid'),
                   ('paid','Paid')],
        default = 'notpaid',readonly=True
    )


    def action_post(self):
        super().action_post()
        # template = self.env.ref('account.email_template_edi_invoice')
        # template.send_mail(self.id,force_send=True)

    # def action_create_payments(self):
    #     self.payment_status == 'paid'
    #     print('qqsawdawdx')
    #     super(FleetInvoice,self).action_create_payments()


 #
 #
 # def write(self, vals):
 #            if 'related_so_ids' in vals:
 #                for invoice in self:
 #                    # Get the previous Sale Orders before update
 #                    previous_sale_orders = invoice.related_so_ids
 #
 #                    # Get the new Sale Orders after update
 #                    new_sale_orders = self.env['sale.order'].browse(
 #                        vals.get('related_so_ids')[0][2])
 #
 #                    # Find the removed Sale Orders
 #                    removed_so = previous_sale_orders - new_sale_orders
 #
 #                    if removed_so:
 #                        # Find invoice lines related to removed Sale Orders
 #                        invoice_lines_to_remove = invoice.invoice_line_ids.filtered(
 #                            lambda
 #                                line: line.sale_line_ids.order_id in removed_so
 #                        )
 #                        invoice_lines_to_remove.unlink()  # Remove them from the invoice
 #
 #            return super().write(vals)
 #
 #        from odoo import models, fields, api
 #
 #        class AccountMove(models.Model):
 #            _inherit = 'account.move'
 #
 #            sale_order_count = fields.Integer(
 #                string="Sales Order Count",
 #                compute="_compute_sale_order_count"
 #            )
 #
 #            @api.depends('invoice_line_ids.sale_line_ids.order_id',
 #                         'related_so_ids')
 #            def _compute_sale_order_count(self):
 #                """
 #                Compute the total number of sales orders linked to the invoice.
 #                Includes both directly related orders and manually selected related_so_ids.
 #                """
 #                for invoice in self:
 #                    sale_orders = invoice.mapped(
 #                        'invoice_line_ids.sale_line_ids.order_id') | invoice.related_so_ids
 #                    invoice.sale_order_count = len(sale_orders)
 #
 #            def action_view_sales_orders(self):
 #                """
 #                Action to open all sales orders related to the invoice.
 #                Includes orders from invoice lines and selected related_so_ids.
 #                """
 #                self.ensure_one()
 #                sale_orders = self.mapped(
 #                    'invoice_line_ids.sale_line_ids.order_id') | self.related_so_ids
 #                return {
 #                    'type': 'ir.actions.act_window',
 #                    'name': 'Sales Orders',
 #                    'res_model': 'sale.order',
 #                    'view_mode': 'tree,form',
 #                    'domain': [('id', 'in', sale_orders.ids)],
 #                    'context': {'default_partner_id': self.partner_id.id},
 #                }
 #            #
 #
 #
 #            def action_view_sales_orders(self):
 #                """
 #                Extend the default action to include related_so_ids.
 #                """
 #                action = super().action_view_sale_orders()  # Call parent method
 #                sale_orders = self.mapped(
 #                    'invoice_line_ids.sale_line_ids.order_id') | self.related_so_ids
 #                action['domain'] = [('id', 'in', sale_orders.ids)]
 #                return action
