# from odoo import api, fields, models
# from odoo.http import request
#
#
# class Website(models.Model):
#     _inherit = 'website'
#
#     @api.model
#     def _search_get_details(self, search_type, order, options):
#         result = super()._search_get_detail(search_type, order, options)
#         user = request.env.user.public_id
#         allowed_products_ids = user.allowed_products_ids
#         if allowed_products_ids:
#             # result
#             result['search_fields'].append('allowed_products_ids')
#
#         return result