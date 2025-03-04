# -*- coding: utf-8 -*-
"""Here we handles Filtering products based on users preference"""
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherit(WebsiteSale):
    """inheriting websitesale controler class to filter products for allowed products and
    allowed category to display in ecommerce shop."""

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
         """ Extend _shop_lookup_products to filter based on allowed products and allowed categories """
         fuzzy_search_term, product_count, search_result = super()._shop_lookup_products( attrib_set, options, post, search, website)
         user = request.env.user
         if user and user.partner_id:
             partner = user.partner_id
             allowed_products = partner.allowed_products_ids
             allowed_category = partner.allowed_category_ids
             # check condition
             if allowed_products:
                 search_result = search_result.filtered(lambda p:p.id in allowed_products.ids)
             elif allowed_category:
                 search_result = request.env['product.template'].search([("categ_id","=",allowed_category.id)])
             product_count = len(search_result)
         return fuzzy_search_term, product_count, search_result
