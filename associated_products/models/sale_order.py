from odoo import api, fields, models, Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    associated_products = fields.Boolean("Associated product")

    @api.onchange('associated_products')
    def _add_associated_products(self):
        if self.associated_products == True:
            for product in self.partner_id.associated_products_ids:
                same_product = self.order_line.filtered(
                    lambda l: l.product_id == product)
                if not same_product:
                       self.order_line = [
                        Command.create({
                            'order_id': self.id,
                            'product_id': product.id,
                            'product_uom_qty': 1,
                            'price_unit': product.lst_price,})]
        else:
            asso_prod_ids = self.partner_id.associated_products_ids
            same_products = self.order_line.filtered(lambda l:l.product_id.id in asso_prod_ids.ids)
            if same_products:
                self.order_line = [fields.Command.delete(record.id) for record in same_products]























            # same_product = self.order_line.filtered(lambda l: l.product_id.id in asso_prod_ids.ids)
            # print("saaaaa",same_product)
            # if same_product:
            #     self.order_line = [fields.Command.delete(rec.id) for rec in same_product]


            # self.order_line = [Command.unlink(self.order_line.ids)]
            # same_product.unlink()



                # if same_product:
                #         self.order_line = [Command.unlink(self.order_line.ids)]

                    # associated_product = self.partner_id.associated_products_ids
                    # print(associated_product)
                    # same_product = self.order_line.filtered(
                    #     lambda l: l.product_id in associated_product)
                    # print(same_product.ids)
                    # for prod in same_product.ids:
                    #     prod.unlink()




    # def action_confirm(self):
    #     value = super(associated_products,self).action_confirm()
    #     if associated_products:
    #         for partner in self.partner_id:
    #             for product in partner.associated_products_ids:
    #                 same_product = self.order_line.filtered(
    #                     lambda l: l.product_id == product)
    #                 if not same_product:
    #                     print(product)
    #                     self.env['sale.order.line'].create({
    #                         'order_id': self.id,
    #                         'product_id': product.id,
    #                         'product_uom_qty': 1,
    #                         'price_unit': product.lst_price,
    #                     })
    #     return value
