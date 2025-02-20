from odoo import api, fields, models, Command


class SaleOrderLine(models.Model):
    _inherit = 'sale.order'

    order

    @api.depends('partner_id.is_orderd_status')
    def _compute_is_orderd(self):
        if self.partner_id.is_orderd == True:
            print('12')
            for product in self.partner_id.orderd_products_ids:
                product_type = self.order_line.search(['invoice_policy','=','order'])
                print(product_type)

            # for record in self:
            #     product_type = record.env['product.product'].search(['invoice_policy','=','order'])
            #     print(product_type)



# order_line
# partner_id

