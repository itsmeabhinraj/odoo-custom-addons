from odoo import http
from odoo.http import request, route
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import lazy

class WebsiteSaleInherit(WebsiteSale):

    @route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        res = super(WebsiteSaleInherit, self).shop(page, category, search, min_price, max_price, ppg, **post)
        user = request.env.user
        print('user',user)
        # apply conditions for filter products
        if user.partner_id.allowed_products_ids:
            print("reached")
            products = request.env['product.template'].search([('id','in',user.partner_id.allowed_products_ids.ids)])
            print('products demo',products)
        else:
            products = request.env['product.template'].search([])
            print('products1', products)
        res.qcontext['products'] = products
        ppg = res.qcontext['ppg']
        ppr = res.qcontext['ppr']
        res.qcontext['bins'] = lazy(lambda: main.TableCompute().process(products, ppg, ppr))
        return res
        # # res.qcontext.update({'products':products})
        # print('bins',res.qcontext['bins'])
        # # res.qcontext['bins'] = products
        # print('bins', res.qcontext['bins'])
        # return res

    # res.qcontext['category'] = category
    # res.qcontext['attributes'] = attributes
    # res.qcontext['search'] = search
    # res.qcontext['pager'] = pager
    # res.qcontext['search_product'] = search_product
    # res.qcontext['products_prices'] = products_prices

    # categ = res.qcontext['categories']
    # print(categ)
    # res.qcontext.update({'categories': categ})

    # website = request.env['website'].get_current_website()
    # fuzzy_search_term, product_count, search_product = self._shop_lookup_products(attrib_set, options, post, search,
    #                                                                              website)

    # res.qcontext['pager'] = website.pager(url=url, total=product_count, page=page, step=ppg, scope=5, url_args=post)
    # if category:
    #     categ = res.qcontext['categories']
    #     res.qcontext.update({'categories': categ})