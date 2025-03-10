import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        // If discount limit setting is disabled, proceed with payment
//        if (!this.config.enable_discount_limits) {
//            return super.pay();
//        }

//        console.log(this.get_order());
//        console.log("Welcome pos page")
        var orderlines = this.get_order().get_orderlines();
//        console.log(orderlines)
        var categoryDiscounts = {};
//        var discount_limited_category =
//        this.models["pos.category"].getFirst().pos_category_id.name;
        orderlines.forEach((line) => {
            //get each product
            console.log('orderlines',orderlines);
            var product = line.get_product();
            console.log('product',product);
            //product discount - in %
            var line_discount = line.get_discount();
            console.log("line_discount",line_discount);

            var unit_qty = line.get_quantity();
            console.log('unit',unit_qty)

            var price_without_discount = line.getUnitDisplayPriceBeforeDiscount();
            console.log('price_without_disco',price_without_discount);
//            var without_discount =
            var get_total_cost = line.get_total_cost();
            console.log("get_total_cost",get_total_cost);

            var unit_price = line.price_unit;
            console.log('unit_price',unit_price);

            var product_categories = product.pos_categ_ids;
            console.log("product_categories",product_categories);

//            product_categories.forEach((category) => {
//                var categ_config = this.pos.categories_by_id[category];
//                if (categ_config && categ_config.has_discount_limit) {
//                    var discount_type = categ_config.discount_type; // 'fixed' or 'percentage'
//                    console.log(discount_type)
//                    var discount_limit = categ_config.discount_limit; // Limit value
//                    console.log(discount_limit)
////
////                    // Initialize category tracking if not set
//                    if (!categoryDiscounts[category]) {
//                        categoryDiscounts[category] = {
//                            discount_amount: 0,
//                            total_unit_price: 0
//                        };
//                    }
//
////                    // Compute applied discount for the category
//                    var applied_discount = (line_price * line_discount) / 100;
//                    categoryDiscounts[category].discount_amount += applied_discount;
//                    categoryDiscounts[category].total_unit_price += line_price / ((100 - line_discount) / 100);
//                }
//            });
        });

//           });

        return super.pay();
    }
});



































//
//
//
//        var orderlines = this.get_order().get_orderlines();
//        var categoryDiscounts = {}; // Store category-wise discount details
//
//        // Loop through order lines and calculate discount per category
//        orderlines.forEach((line) => {
//            var product = line.get_product();
//            var line_discount = line.get_discount();
//            var line_price = line.price_subtotal;
//            var product_categories = product.pos_categ_ids;
//
//            product_categories.forEach((categ_id) => {
//                // Fetch category discount settings directly from pos.category
//                var categ_config = this.pos.categories_by_id[categ_id];
//                if (categ_config && categ_config.has_discount_limit) {
//                    var discount_type = categ_config.discount_type; // 'fixed' or 'percentage'
//                    var discount_limit = categ_config.discount_limit; // Limit value
//
//                    // Initialize category tracking if not set
//                    if (!categoryDiscounts[categ_id]) {
//                        categoryDiscounts[categ_id] = {
//                            discount_amount: 0,
//                            total_unit_price: 0
//                        };
//                    }
//
//                    // Compute applied discount for the category
//                    var applied_discount = (line_price * line_discount) / 100;
//                    categoryDiscounts[categ_id].discount_amount += applied_discount;
//                    categoryDiscounts[categ_id].total_unit_price += line_price / ((100 - line_discount) / 100);
//                }
//            });
//        });
//
//        // Validate discount limits per category
//        for (const categ_id in categoryDiscounts) {
//            var categ_config = this.pos.categories_by_id[categ_id];
//            var discount_type = categ_config.discount_type;
//            var discount_limit = categ_config.discount_limit;
//            var applied_discount = categoryDiscounts[categ_id].discount_amount;
//            var total_unit_price = categoryDiscounts[categ_id].total_unit_price;
//
//            if (discount_type === "percentage") {
//                var applied_discount_percent = (applied_discount / total_unit_price) * 100;
//                if (applied_discount_percent > discount_limit) {
//                    this.dialog.add(AlertDialog, {
//                        title: _t("Warning"),
//                        body: _t(The applied discount (${applied_discount_percent.toFixed(2)}%) exceeds the allowed limit (${discount_limit}%) for this category.),
//                    });
//                    return;
//                }
//            } else if (discount_type === "fixed") {
//                var discounted_total = total_unit_price - applied_discount;
//                if (discounted_total < discount_limit) {
//                    this.dialog.add(AlertDialog, {
//                        title: _t("Warning"),
//                        body: _t(The applied discount amount exceeds the allowed fixed limit for this category.),
//                    });
//                    return;
//                }
//            }
//        }

        // Proceed with payment if discount limits are not exceeded
//        return super.pay();
//    }
//});