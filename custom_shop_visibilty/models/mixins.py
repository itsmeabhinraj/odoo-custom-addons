# -*- coding: utf-8 -*-
"""customizing searching functionality in ecommerce shop website. Now allowed_products and
         allowed category can be get throug search function """
from odoo import api, models

class WebsiteSearchableMixinInherit(models.AbstractModel):
    """inheriting WebsiteSearchableMixin for customize search options"""

    _inherit = 'website.searchable.mixin'

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
         """By using _search_fetch() , we can override it and add additional domain as our purpose."""
         results,count = super()._search_fetch(search_detail, search, limit, order)
         user = self.env.user
         if user.partner_id.allowed_products_ids:
              partner = user.partner_id
              allowed_products = partner.allowed_products_ids
              allowed_category = partner.allowed_category_ids
              # Apply filtering to search results
              domain = []
              if allowed_products:
                  domain.append(('id', 'in', allowed_products.ids))
              if allowed_category:
                  domain.append(('categ_id', 'in', allowed_category.ids))
              model = self.sudo() if search_detail.get('requires_sudo') else self
              results = model.search(domain,limit=limit,order=search_detail.get('order', order))
              count = model.search_count(domain)
         return results, count
