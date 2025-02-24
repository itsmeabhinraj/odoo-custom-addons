from odoo import api,fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_ids = fields.Many2many('account.move')
    invoice_count = fields.Integer(string="Invoice Count",compute='_compute_invoices_count')
    invoice_id = fields.Many2one('account.move')
    invoices = fields.Char()
    # related_so_ids = fields.Many2many('account.move')

    #  final code

    def action_view_invoice(self,invoices=False):
        self.ensure_one()
        normal_invoices = self.env['account.move'].search([
            ('invoice_origin', '=', self.name)
        ])
        # print('normal_invoices',nor`mal_invoices)
        related_invoices = self.env['account.move'].search([
            ('related_so_ids', 'in', self.id)
        ])
        # print(related_invoices)
        # print('invoices',invoices)
        return {
            'name': 'Related Invoices',
            'type': 'ir.actions.act_window',
            'view_mode': 'list, form',
            'res_model': 'account.move',
            'res_id': False,
            # 'domain': [('id', 'in', invoices.ids)],
            'domain': [('id', 'in', normal_invoices.ids + related_invoices.ids)],
            'context': {'create': False},
        }
        super().action_view_invoice()

    def _compute_invoices_count(self):
        for record in self:
            normal_invoices = self.env['account.move'].search([('invoice_origin','=',record.name)])
            related_invoices = self.env['account.move'].search([('related_so_ids','in',record.id)])
            record.invoice_count = len(normal_invoices | related_invoices)
            print(normal_invoices)
            print(related_invoices)
            print(record.invoice_count)

