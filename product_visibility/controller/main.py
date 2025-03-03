# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.tools import lazy


class ProductVisibility(WebsiteSale):
    """Class defined for customizing the shop page in the website"""

    @http.route()
    def shop(self, category=None, ppg=False):
        """Function defined for showing only the selected
         products for thr logged in customer"""
        res = super(ProductVisibility, self).shop(self, category=category)
        user = request.env.user
        categ = user.allowed_category_ids
        product = request.env['product.template'].search(
                    [('public_categ_ids', 'in', categ.ids)])
        p_count = request.env['product.template'].search_count(
                    [('public_categ_ids', 'in', categ.ids)])
        res.qcontext['pager']['page_count'] = 1

        products_prices = res.qcontext.get("products_prices")
        print('product_prices', products_prices)
        allowed_product_ids = user.partner_id.allowed_product_ids
        for rec in allowed_product_ids:
            products_prices[rec.id] = {'price_reduce': rec.list_price}
        res.qcontext["products_prices"] = products_prices

        categ_bins = lazy(lambda: TableCompute().process(product, ppg or 20))
        print("helo")
        bins = lazy(lambda: TableCompute().process(user.allowed_product_ids, ppg=1))
        pricelist = request.env['product.pricelist'].browse(
            request.session.get('website_sale_current_pl'))
        products_prices = lazy(lambda: product._get_sales_prices(pricelist))
        if user.allowed_product_ids:
            for rec in user.allowed_product_ids:
                res.qcontext.update({
                    'products': rec,
                    'category': rec.public_categ_ids,
                    'pricelist': pricelist,
                    'bins': bins,
                })
        elif user.allowed_category_ids:
            res.qcontext.update({
                'search_product': product,
                'products': product,
                'categories': user.allowed_category_ids,
                'search_count': p_count,
                'pricelist': pricelist,
                'get_product_prices': lambda product: lazy(
                    lambda: products_prices[product.id]),
                'bins': categ_bins,
            })
        return res
    # def _shop_lookup_products(self, search, category, attrib_values, offset, limit, order, min_price, max_price):
    #     domain = [('sale_ok', '=', True), ('website_published', '=', True)]
    #
    #     partner = request.env.user.partner_id
    #     if partner:
    #         allowed_product_ids = partner.allowed_product_ids.ids
    #         allowed_category_ids = partner.allowed_category_ids.ids
    #
    #         # Apply product and category restrictions if set
    #         if allowed_product_ids and allowed_category_ids:
    #             domain.append('|')  # OR condition between product and category
    #             domain.append(('id', 'in', allowed_product_ids))
    #             domain.append(('public_categ_ids', 'in', allowed_category_ids))
    #         elif allowed_product_ids:
    #             domain.append(('id', 'in', allowed_product_ids))
    #         elif allowed_category_ids:
    #             domain.append(('public_categ_ids', 'in', allowed_category_ids))
    #
    #     products = request.env['product.template'].search(domain, offset=offset, limit=limit, order=order)
    #     return products