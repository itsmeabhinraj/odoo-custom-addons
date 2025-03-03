
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
        categ = user.product_category_ids
        product = request.env['product.template'].search(
                    [('public_categ_ids', 'in', categ.ids)])
        p_count = request.env['product.template'].search_count(
                    [('public_categ_ids', 'in', categ.ids)])
        res.qcontext['pager']['page_count'] = 1
        categ_bins = lazy(lambda: TableCompute().process(product, ppg))
        bins = lazy(
            lambda: TableCompute().process(user.product_ids, ppg=1))
        pricelist = request.env['product.pricelist'].browse(
            request.session.get('website_sale_current_pl'))
        products_prices = lazy(lambda: product._get_sales_prices(pricelist))
        if user.product_ids:
            for rec in user.product_ids:
                res.qcontext.update({
                    'products': rec,
                    'category': rec.public_categ_ids,
                    'bins': bins,
                })
        elif user.product_category_ids:
            res.qcontext.update({
                'search_product': product,
                'products': product,
                'categories': user.product_category_ids,
                'search_count': p_count,
                'pricelist': pricelist,
                'get_product_prices': lambda product: lazy(
                    lambda: products_prices[product.id]),
                'bins': categ_bins,
            })
        return res


def _get_search_options(self, category=None, attrib_values=None, tags=None, min_price=0.0, max_price=0.0,
                        conversion_rate=1, allowed_product_ids=None, **post):
    options = super()._get_search_options(category, attrib_values, min_price, max_price, tags, conversion_rate, **post)

    partner = request.env.user.partner_id if request.env.user else None
    allowed_product_ids = partner.allowed_products_ids.ids if partner and partner.allowed_products_ids else []

    if allowed_product_ids:
        options['allowed_product_ids'] = allowed_product_ids

    return options


@route([
    '/shop',
    '/shop/page/<int:page>',
    '/shop/category/<model("product.public.category"):category>',
    '/shop/category/<model("product.public.category"):category>/page/<int:page>',
], type='http', auth="public", website=True)
def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
    res = super(WebsiteSaleInherit, self).shop(page, category, search, min_price, max_price, ppg, **post)

    partner = request.env.user.partner_id if request.env.user else None
    allowed_product_ids = partner.allowed_products_ids.ids if partner and partner.allowed_products_ids else []

    # Build domain for allowed products
    domain = []
    if allowed_product_ids:
        domain.append(('id', 'in', allowed_product_ids))

    # Apply category, price, and search filters
    if category:
        domain.append(('categ_id', '=', category.id))
    if min_price:
        domain.append(('list_price', '>=', min_price))
    if max_price:
        domain.append(('list_price', '<=', max_price))
    if search:
        domain.append(('name', 'ilike', search))

    # Fetch the filtered products
    products = request.env['product.template'].search(domain)

    res.qcontext['products'] = products
    ppg = res.qcontext['ppg']
    ppr = res.qcontext['ppr']
    res.qcontext['bins'] = lazy(lambda: main.TableCompute().process(products, ppg, ppr))

    return res

class WebsiteSaleCustom(WebsiteSale):

    def _shop_lookup_products(self, search, category, attrib_values, offset, limit, order, min_price, max_price):
        domain = [('sale_ok', '=', True), ('website_published', '=', True)]

        partner = request.env.user.partner_id
        if partner:
            allowed_product_ids = partner.allowed_product_ids.ids
            allowed_category_ids = partner.allowed_category_ids.ids

            # Apply product and category restrictions if set
            if allowed_product_ids and allowed_category_ids:
                domain.append('|')  # OR condition between product and category
                domain.append(('id', 'in', allowed_product_ids))
                domain.append(('public_categ_ids', 'in', allowed_category_ids))
            elif allowed_product_ids:
                domain.append(('id', 'in', allowed_product_ids))
            elif allowed_category_ids:
                domain.append(('public_categ_ids', 'in', allowed_category_ids))

        products = request.env['product.template'].search(domain, offset=offset, limit=limit, order=order)
        return products