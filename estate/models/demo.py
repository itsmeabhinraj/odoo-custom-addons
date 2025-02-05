# for sale_order in self.related_so_ids:
#             sale_order.write({'invoice_id': self.id})  # Link invoice to SO
#
#             for order_line in sale_order.order_line:
#
# invoice
#
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
#
#
# <xpath expr="//div[@name='button_box']" position="inside">
#             <button name="action_view_invoice"
#                     type="object"
#                     class="oe_stat_button"
#                     icon="fa-file-invoice">
#                 <field name="invoice_id"/>
#                 <div class="o_stat_info">
#                     <span class="o_stat_text">Invoice</span>
#                 </div>
#             </button>
#         </xpath>



def action_view_invoice(self):
    """ Open the corresponding invoice from the Sale Order smart button """
    self.ensure_one()
    if self.invoice_id:
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'context': {'create': False},
        }



action_view_related_sales_orders(self):
        """ Open the related sale orders in a list and form view from the smart button. """
        return {
            'name': 'Related Sales Orders',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('id', 'in', self.related_so_ids.ids)],
            'context': {'create': False},
        }









class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_ids = fields.Many2many(
        "account.move",
        string="Invoices",
        compute="_compute_invoices",
        store=True,
    )

    invoice_count = fields.Integer(
        string="Invoice Count",
        compute="_compute_invoices",
        store=True,
    )

    @api.depends("order_line.move_ids", "related_so_ids")
    def _compute_invoices(self):
        for order in self:
            # Fetch invoices from the sale order lines and related sale orders
            invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('out_invoice', 'out_refund'))
            related_invoices = order.related_so_ids.mapped("invoice_ids")  # Get invoices from related SOs

            # Combine invoices from the current SO and its related SOs
            order.invoice_ids = invoices | related_invoices
            order.invoice_count = len(order.invoice_ids)
def action_view_invoice(self):
    action = self.env.ref("account.action_move_out_invoice_type").read()[0]
    action["domain"] = [("id", "in", self.invoice_ids.ids)]
    return action

#
#
def action_view_related_invoices(self):
    '''Action to view related invoices'''
    self.ensure_one()
    # Find invoices created through normal workflow
    normal_invoices = self.env['account.move'].search([
        ('invoice_origin', '=', self.name)
    ])
    # Find invoices where this Sale Order is in related_so_ids
    related_invoices = self.env['account.move'].search([
        ('related_so_ids', 'in', self.id)
    ])
    # Combine both
    invoices = normal_invoices | related_invoices
    return {
        'name': 'Related Invoices',
        'type': 'ir.actions.act_window',
        'view_mode': 'tree,form',
        'res_model': 'account.move',
        'domain': [('id', 'in', invoices.ids)],
        'context': {'create': False},
    }


<record id="sale_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <!-- Add smart button for related Invoices -->
        <xpath expr="//sheet" position="inside">
            <div class="oe_button_box" name="button_box">
                <button
                    class="oe_stat_button"
                    type="object"
                    name="action_view_related_invoices"
                    icon="fa-file-invoice"
                    string="Related Invoices"
                    attrs="{'invisible': [('invoice_count', '=', 0)]}">
                    <field name="invoice_count" widget="statinfo" string="Invoices"/>
                </button>
            </div>
        </xpath>
    </field>
</record>