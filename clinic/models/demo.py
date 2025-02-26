from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Get the current logged-in user
        user = self.env.user
        allowed_products = user.partner_id.allowed_product_ids

        # Filter products if allowed products exist for the user
        if allowed_products:
            args.append(('id', 'in', allowed_products.ids))

        return super(ProductTemplate, self).search(args, offset, limit, order, count)

#     < record
#     id = "view_product_product_filter_allowed"
#     model = "ir.ui.view" >
#     < field
#     name = "name" > product.template.shop.allowed.filter < / field >
#     < field
#     name = "model" > product.template < / field >
#     < field
#     name = "inherit_id"
#     ref = "website_sale.products_list_view" / >
#     < field
#     name = "arch"
#     type = "xml" >
#     < xpath
#     expr = "//div[@class='o_shop_products']"
#     position = "attributes" >
#     < attribute
#     name = "domain" > [('id', 'in', user.partner_id.allowed_product_ids.ids)] < / attribute >
#
# < / xpath >
# < / field >
# < / record >