from gevent._util import Lazy
from validators import domain
from werkzeug.exceptions import NotFound

from addons.website_sale.controllers.main import TableCompute
from odoo import http
from odoo.http import request, route
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import lazy

class WebsiteSaleInherit(WebsiteSale):
    # def _get_search_options(
    #     self, category=None, attrib_values=None, min_price=0.0, max_price=0.0,
    #     conversion_rate=1, allowed_product_ids=None, **post):
    #     """ Extend search options to filter products by allowed_product_ids """
    #     options = super()._get_search_options(category, attrib_values, min_price, max_price, conversion_rate, **post)
    #     # Add filtering by allowed products if applicable
    #     if allowed_product_ids:
    #         print(allowed_product_ids)
    #         options['allowed_product_ids'] = allowed_product_ids
    #     return options
    #
    # def _shop_lookup_products(self, attrib_set, options, post, search, website):
    #      """ Extend _shop_lookup_products to filter based on allowed products """
    #      fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(attrib_set, options, post, search, website)
    #      # Filter products based on allowed_product_ids if available
    #      allowed_product_ids = options.get('allowed_product_ids')
    #      if allowed_product_ids:
    #         search_result = search_result.filtered(lambda p: p.id in allowed_product_ids)
    #
    #      return fuzzy_search_term, len(search_result), search_result

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
        partner = request.env.user.partner_id if request.env.user else None
        # res_user_object = request.env['res.partner'].sudo().browse(request.uid)
        # allowed_products_ids = partner.allowed_products_ids.ids if partner and partner.allowed_products_ids else None
        allowed_products_ids = partner.allowed_products_ids
        print(res.qcontext)
        website = request.env['website'].get_current_website()
        pricelist = website.pricelist_id
        # products_prices = lazy(lambda: product._get_sales_prices(pricelist))

        products_prices = res.qcontext.get("products_prices")
        print('product_prices',products_prices)
        for rec in allowed_products_ids:
            products_prices[rec.id] = {'price_reduce': rec.list_price}
        res.qcontext["products_prices"] = products_prices

        domain = []
        if user.partner_id.allowed_products_ids:
            print("reached")
            # products = request.env['product.template'].search([('id','in',user.partner_id.allowed_products_ids.ids)])
            domain.append(('id','in',user.partner_id.allowed_products_ids.ids))

            if search:
                domain.append(('name', 'ilike', search))

            products = request.env['product.template'].search(domain)
            res.qcontext['products']= products
            res.qcontext['categories'] = products.public_categ_ids
            res.qcontext['attributes'] = products.attribute_line_ids.attribute_id
            res.qcontext['search_product'] = products
            res.qcontext['search_count'] = len(products)
            ppg = res.qcontext['ppg']
            ppr = res.qcontext['ppr']
            bins = lazy(lambda: main.TableCompute().process(products, ppg, ppr))

            products_prices = res.qcontext.get("products_prices")
            for rec in products:
                products_prices[rec.id] = {'price_reduce': rec.list_price}
            res.qcontext["products_prices"] = products_prices
            # category
            product_template_list = []
            if res.qcontext["category"]:
                for record in products:
                    if res.qcontext["category"].id in record.public_categ_ids.ids:
                        product_template_list.append(record.id)
                product_template = request.env["product.template"].sudo().browse(product_template_list)

                res.qcontext["products"] = product_template
                res.qcontext["search_product"] = product_template
                res.qcontext["search_count"] = len(product_template)
                res.qcontext["bins"] = Lazy(lambda: TableCompute().process(product_template,
                    res.qcontext.get("ppg"),
                    res.qcontext.get("ppp")
                ))
            # Attribute applied
            attribute_list = []
            if res.qcontext["attrib_set"]:
                for val in res.qcontext["attrib_set"]:
                    attribute_list.append(val)

            for record in products.attribute_line_ids:
                for value in record.value_ids.ids:
                    if value in attribute_list:
                        products = products.filtered(lambda l: value in l.attribute_line_ids.value_ids.ids)
                        res.qcontext["products"] = products
                        res.qcontext["search_product"] = products
                        res.qcontext["search_count"] = len(products)

            # pager
            website = request.env["website"].get_current_website()
            page = website.pager(url='/shop', total=res.qcontext.get("search_count"), page=page,
                                 step=res.qcontext.get("ppg"), scope=res.qcontext.get("ppg"), url_args=post)
            offset = page["offset"]
            products_on_page = res.qcontext.get("search_product")[offset:offset + res.qcontext.get("ppg")]
            res.qcontext["ppg"] = page
            res.qcontext["bins"] = Lazy(lambda: TableCompute().process(products_on_page,
                    res.qcontext.get("ppg"),
                    res.qcontext.get("ppp")
                )
            )
            for product in user.allowed_products_ids:
                res.qcontext.update({'bins':bins,'products':products,'category': product.public_categ_ids,})
            print('print',res.qcontext['bins'])
        return res

















#
#
# # --------
# # res = super(WebsiteSaleInherit, self).shop(page, category, search, min_price, max_price, ppg, **post)
# #         user = request.env.user
# #         print('user',user)
# #         partner = request.env.user.partner_id if request.env.user else None
# #         allowed_products_ids = partner.allowed_products_ids.ids if partner and partner.allowed_products_ids else None
# #         # apply conditions for filter products
# #         domain = []
# #         if user.partner_id.allowed_products_ids:
# #             print("reached")
# #             # products = request.env['product.template'].search([('id','in',user.partner_id.allowed_products_ids.ids)])
# #             domain.append(('id','in',user.partner_id.allowed_products_ids.ids))
# #             # print('products demo',products)
# #             # res.qcontext['products'] = products
# #             # Category = request.env['product.public.category']
# #             # if category:
# #             #     category = Category.search([('id', '=', int(category))], limit=1)
# #             #     print(category)
# #             #     if not category or not category.can_access_from_current_website():
# #             #         raise NotFound()
# #             # else:
# #             #     category = Category
# #             if category:
# #                 domain.append(('categ_id', '=', category.id))
# #             if search:
# #                 domain.append(('name', 'ilike', search))
# #             products = request.env['product.template'].search(domain)
# #             res.qcontext['products']= products
# #             ppg = res.qcontext['ppg']
# #             ppr = res.qcontext['ppr']
# #             res.qcontext['bins'] = lazy(lambda: main.TableCompute().process(products, ppg, ppr))
# #             print(res.qcontext['bins'])
# #         return res
# # --------
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # new one
# # from odoo.addons.website_sale.controllers.main import WebsiteSale
# # from odoo import http
# # from odoo.http import request, route
# # from odoo.osv import expression
# #
# # class CustomWebsiteSale(WebsiteSale):
# #     def _get_search_options(
# #         self, category=None, attrib_values=None, min_price=0.0, max_price=0.0,
# #         conversion_rate=1, allowed_product_ids=None, **post):
# #         """ Extend search options to filter products by allowed_product_ids """
# #         options = super()._get_search_options(category, attrib_values, min_price, max_price, conversion_rate, **post)
# #         # Add filtering by allowed products if applicable
# #         if allowed_product_ids:
# #              options['allowed_product_ids'] = allowed_product_ids
# #         return options
# #
# #     def _shop_lookup_products(self, attrib_set, options, post, search, website):
# #          """ Extend _shop_lookup_products to filter based on allowed products """
# #          fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(attrib_set, options, post, search, website)
# #          # Filter products based on allowed_product_ids if available
# #          allowed_product_ids = options.get('allowed_product_ids')
# #          if allowed_product_ids:
# #             search_result = search_result.filtered(lambda p: p.id in allowed_product_ids)
# #
# #          return fuzzy_search_term, len(search_result), search_result
# #
# #
# #     @route([
# #     '/shop',
# #     '/shop/page/<int:page>',
# #     '/shop/category/<model("product.public.category"):category>',
# #     '/shop/category/<model("product.public.category"):category>/page/<int:page>',
# #      ], type='http', auth="public", website=True)
# #     def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
# #         """ Inherit and optimize shop() for filtering allowed products """
# #
# #         # Check if the user is logged in
# #         partner = request.env.user.partner_id if request.env.user else None
# #         allowed_products_ids = partner.allowed_products_ids.ids if partner and partner.allowed_products_ids else None
# #
# #         # Get standard shop filters and search options
# #         website = request.env['website'].get_current_website()
# #         website_domain = website.website_domain()
# #         attrib_list = request.httprequest.args.getlist('attribute_value')
# #         attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
# #         attrib_set = {v[1] for v in attrib_values}
# #
# #         # Apply search options, including filtering by allowed products
# #         options = self._get_search_options(
# #             category=category,
# #             attrib_values=attrib_values,
# #             min_price=min_price,
# #             max_price=max_price,
# #             conversion_rate=1,
# #             allowed_products_ids=allowed_products_ids,
# #             **post
# #         )
# #
# #         # Get products
# #         fuzzy_search_term, product_count, search_product = self._shop_lookup_products(attrib_set, options, post, search, website)
# #
# #         # Pagination
# #         ppg = int(ppg) if ppg else website.shop_ppg or 20
# #         pager = website.pager(url='/shop', total=product_count, page=page, step=ppg, scope=5, url_args=post)
# #         offset = pager['offset']
# #         products = search_product[offset:offset + ppg]
# #
# #         # Render shop template
# #         values = {
# #             'search': fuzzy_search_term or search,
# #             'products': products,
# #             'pager': pager,
# #             'category': category,
# #             'attrib_values': attrib_values,
# #             'attrib_set': attrib_set,
# #             'search_count': product_count,
# #             'layout_mode': request.session.get('website_sale_shop_layout_mode', 'grid'),
# #             'ppg': ppg,
# #         }
# #
# #         return request.render("website_sale.products", values)
#
#
#
#
#
# # old one
# # from odoo import http
# # from odoo.http import request, route
# # from odoo.addons.website_sale.controllers import main
# # from odoo.addons.website_sale.controllers.main import WebsiteSale
# # from odoo.tools import lazy
# #
# # class WebsiteSaleInherit(WebsiteSale):
# #
# #     @route([
# #         '/shop',
# #         '/shop/page/<int:page>',
# #         '/shop/category/<model("product.public.category"):category>',
# #         '/shop/category/<model("product.public.category"):category>/page/<int:page>',
# #     ], type='http', auth="public", website=True)
# #     def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
# #         res = super(WebsiteSaleInherit, self).shop(page, category, search, min_price, max_price, ppg, **post)
# #         user = request.env.user
# #         print('user',user)
# #         # apply conditions for filter products
# #         if user.partner_id.allowed_products_ids:
# #             print("reached")
# #             products = request.env['product.template'].search([('id','in',user.partner_id.allowed_products_ids.ids)])
# #             print('products demo',products)
# #         else:
# #             products = request.env['product.template'].search([])
# #             print('products1', products)
# #         res.qcontext['products'] = products
# #         ppg = res.qcontext['ppg']
# #         ppr = res.qcontext['ppr']
# #         res.qcontext['bins'] = lazy(lambda: main.TableCompute().process(products, ppg, ppr))
# #         return res
#
#
#
#
#         # # res.qcontext.update({'products':products})
#         # print('bins',res.qcontext['bins'])
#         # # res.qcontext['bins'] = products
#         # print('bins', res.qcontext['bins'])
#         # return res
#
#     # res.qcontext['category'] = category
#     # res.qcontext['attributes'] = attributes
#     # res.qcontext['search'] = search
#     # res.qcontext['pager'] = pager
#     # res.qcontext['search_product'] = search_product
#     # res.qcontext['products_prices'] = products_prices
#
#     # categ = res.qcontext['categories']
#     # print(categ)
#     # res.qcontext.update({'categories': categ})
#
#     # website = request.env['website'].get_current_website()
#     # fuzzy_search_term, product_count, search_product = self._shop_lookup_products(attrib_set, options, post, search,
#     #                                                                              website)
#
#     # res.qcontext['pager'] = website.pager(url=url, total=product_count, page=page, step=ppg, scope=5, url_args=post)
#     # if category:
#     #     categ = res.qcontext['categories']
#     #     res.qcontext.update({'categories': categ})
#
#
#
#     # safe code
#     # @route([
#     #     '/shop',
#     #     '/shop/page/<int:page>',
#     #     '/shop/category/<model("product.public.category"):category>',
#     #     '/shop/category/<model("product.public.category"):category>/page/<int:page>',
#     # ], type='http', auth="public", website=True)
#     # def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
#     #     res = super(WebsiteSaleInherit, self).shop(page, category, search, min_price, max_price, ppg, **post)
#     #     user = request.env.user
#     #     print('user',user)
#     #     partner = request.env.user.partner_id if request.env.user else None
#     #     allowed_products_ids = partner.allowed_products_ids.ids if partner and partner.allowed_products_ids else None
#     #     # apply conditions for filter products
#     #     if user.partner_id.allowed_products_ids:
#     #         print("reached")
#     #         products = request.env['product.template'].search([('id','in',user.partner_id.allowed_products_ids.ids)])
#     #         print('products demo',products)
#     #         res.qcontext['products'] = products
#     #         ppg = res.qcontext['ppg']
#     #         ppr = res.qcontext['ppr']
#     #         res.qcontext['bins'] = lazy(lambda: main.TableCompute().process(products, ppg, ppr))
#     #     return res
#
#
#
#
# # res = super(ProductVisibility, self).shop(self, category=category)
# #         user = request.env.user
# #         categ = user.product_category_ids
# #         product = request.env['product.template'].search(
# #                     [('public_categ_ids', 'in', categ.ids)])
# #         p_count = request.env['product.template'].search_count(
# #                     [('public_categ_ids', 'in', categ.ids)])
# #         res.qcontext['pager']['page_count'] = 1
# #         categ_bins = lazy(lambda: TableCompute().process(product, ppg))
# #         bins = lazy(
# #             lambda: TableCompute().process(user.product_ids, ppg=1))
# #         pricelist = request.env['product.pricelist'].browse(
# #             request.session.get('website_sale_current_pl'))
# #         products_prices = lazy(lambda: product._get_sales_prices(pricelist))
# #         if user.product_ids:
# #             for rec in user.product_ids:
# #                 res.qcontext.update({
# #                     'products': rec,
# #                     'category': rec.public_categ_ids,
# #                     'bins': bins,
# #                 })
# #         elif user.product_category_ids:
# #             res.qcontext.update({
# #                 'search_product': product,
# #                 'products': product,
# #                 'categories': user.product_category_ids,
# #                 'search_count': p_count,
# #                 'pricelist': pricelist,
# #                 'get_product_prices': lambda product: lazy(
# #                     lambda: products_prices[product.id]),
# #                 'bins': categ_bins,
# #             })