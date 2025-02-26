from odoo import http
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherit(WebsiteSale):

    @route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
        user = request.env.user
        # partner_id = request.env.user.partner_id
        partner = user.partner_id
        print('user',user)
        print('partner',partner)
        xxx = partner.allowed_products_ids
        print('user',xxx)
        # for record in
        if user.partner_id.allowed_products_ids:
            print("reached")
            products = request.env['product.product'].search([('id','=',user.partner_id.allowed_products_ids.ids)])
            print('products',products)
        else:
            products = request.env['product.product'].search([])
        # allowed_products = user.partner_id.allowed_product_ids
        # print("Inherited ....", res)
        return request.render("website_sale.products",{'values':{'products':products}})
