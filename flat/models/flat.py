# from odoo import fields,models
#
# class Flat(models.Model):
#     _name = 'flat'
#     _description = 'flat managemnt module'
#
#     flat_id = fields.Many2one('flat.management', string='flats ordered')
#     name = fields.Char('Flat', required=True)
#     flat_description = fields.Text('Description')
#     flat_amount = fields.Float('Price', copy=False, required=True)
#
#
#
#
#
#
#
# import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
# import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
# import { patch } from "@web/core/utils/patch";
#
#
# patch(PosOrderline.prototype, {
#     setup(vals) {
#         this.brand_id = this.product_id.brand_id || "";
#         return super.setup(...arguments);
#     },
#     getDisplayData() {
#         return {
#             ...super.getDisplayData(),
#             brand: this.brand_id.name || "",
#         };
#     },
# });
#
# patch(Orderline, {
#     props: {
#         ...Orderline.props,
#         line: {
#             ...Orderline.props.line,
#             shape: {
#                 ...Orderline.props.line.shape,
#                 brand: { type: String, optional: true },
#             },
#         },
#     },
# });
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
#
#
#
#
#
# <?xml version="1.0" encoding="UTF-8"?>
# <templates id="template" xml:space="preserve">
#     <t t-name="productbrand.Orderline" t-inherit="point_of_sale.Orderline" t-inherit-mode="extension">
#         <xpath expr="//div[hasclass('product-name')]" position="after">
#             <t t-if="props.line.brand">
#                 <div class="product-brand" style="margin-right:10px;">
#                     <t t-esc="'Brand : ' + line.brand"/>
#                 </div>
#             </t>
#         </xpath>
#     </t>
# </templates>





# from odoo import models,api,fields
#
#
# class PosSession(models.Model):
#     """Inherit pos.session to load product.brand data."""
#     _inherit = 'pos.session'
#
#     @api.model
#     def _load_pos_data_models(self, config_id):
#         """Load the data into pos.config.models"""
#         data = super()._load_pos_data_models(config_id)
#         data += ['product.brand']
#         return data