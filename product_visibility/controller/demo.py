from odoo.http import request


class WebsiteShop(WebsiteSale):

    def shop(self, page=0, category=None, search='', min_price=0.0,max_price=0.0):
        res = super(WebsiteShop,self).shop(page, category, search,min_price,max_price,ppg,**post)
        res_user_object = request.env['res.partner'].sudo().browse(request.uid)
        if res_user_object.partner_id.allowed_product_ids:
            product_template_object = res_user_object.partner_id.allowed_product_ids
        elif res_user_object.partner_id.allowed_category_ids:
            product_template_object = request.env['product.template'].search([]).filtered(lambda l: any(cat_id in res_user_object.partner_id.allowed_category_ids.ids for cat_id in l.public_categ_ids.ids))
        else:
            product_template_object = request.env['product.template'].search([])
        res.qcontext['products'] = product_template_object
        res.qcontext['categories'] = product_template_object.public_categ_ids
        res.qcontext['attributes'] = product_template_object.attribute_line_ids.attribute_id
        res.qcontext['search_product'] = product_template_object
        res.qcontext['search_count'] = len(product_template_object)
        x = res.qcontext.get("products_prices")
        for rec in product_template_object:
            x[rec.id] = {'price_reduce': rec.list_price}
        res.qcontext["products_prices"] = x

        # Category applied
        product_template_list = []
        if res.qcontext["category"]:
            chosen_category_id = res.qcontext["category"].id
            for rec in product_template_object:
                if chosen_category_id in rec.public_categ_ids.ids:
                    product_template_list.aqppend(rec.id)
            product_template = request.env["product.template"].sudo().browse(product_template_list)

            res.qcontext["products"] = product_template
            res.qcontext["search_product"] = product_template
            res.qcontext["search_count"] = len(product_template)
            res.qcontext["bins"] = Lazy(lambda: TableCompute().process(
                product_template,
                res.qcontext.get("ppg"),
                res.qcontext.get("ppp")
            ))

        # Attribute applied
        attribute_list = []
        if res.qcontext["attrib_set"]:
            for val in res.qcontext["attrib_set"]:
                attribute_list.append(val)

        for rec in product_template_object.attribute_line_ids:
            for x in rec.value_ids.ids:
                if x in attribute_list:
                    products = product_template_object.filtered(lambda l: x in l.attribute_line_ids.value_ids.ids)
                    res.qcontext["products"] = products
                    res.qcontext["search_product"] = products
                    res.qcontext["search_count"] = len(products)

        # Pager
        website = request.env["website"].get_current_website()
        page = website.pager(url='/shop', total=res.qcontext.get("search_count"), page=page,
                             step=res.qcontext.get("ppg"), scope=res.qcontext.get("ppg"), url_args=post)
        offset = page["offset"]
        products_on_page = res.qcontext.get("search_product")[offset:offset + res.qcontext.get("ppg")]

        res.qcontext["ppg"] = page
        res.qcontext["bins"] = Lazy(
            lambda: TableCompute().process(
                products_on_page,
                res.qcontext.get("ppg"),
                res.qcontext.get("ppp")
            )
        )

        # Filter applied
        if res.qcontext["order"] == "list_price asc":
            products_on_page = products_on_page.sorted(lambda l: l.list_price)
        elif res.qcontext["order"] == "list_price desc":
            products_on_page = products_on_page.sorted(lambda l: l.list_price, reverse=True)
        elif res.qcontext["order"] == "create_date desc":
            products_on_page = products_on_page.sorted(lambda l: l.create_date, reverse=True)

        res.qcontext["bins"] = Lazy(
            lambda: TableCompute().process(
                products_on_page,
                res.qcontext.get("ppg"),
                res.qcontext.get("ppp")
            )
        )
