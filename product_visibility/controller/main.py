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
