/** @odoo-module **/
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        var orderlines = this.get_order().get_orderlines();
//        var product = line.get_product();
//        var product_categories = product.pos_categ_ids;
        var categoryDiscounts = {};
        var totalDiscountedPrice = 0
        var totalOriginalPrice = 0
        //iterate through orderlines
        orderlines.forEach((line) => {
//            var categories = [];
//            line.product_id.pos_categ_ids.forEach((category) => {
//                categories.push(category.name);
//            });
//            console.log('categoried',categories);
            console.log('orderlines',orderlines);
            var product = line.get_product();
            console.log('product',product)
            //product discount - in %
            var line_discount = line.get_discount();
            console.log("line_discount",line_discount);

            var unit_qty = line.get_quantity();
            console.log('unit',unit_qty)

            var price_without_discount = line.getUnitDisplayPriceBeforeDiscount() * unit_qty;
            console.log('price_without_disco',price_without_discount);

            var price_subtotal = line.price_subtotal;
            console.log('price_subtotal',price_subtotal);

            var product_categories = product.pos_categ_ids;
            console.log("product_categories",product_categories);
            //final price of product after tax (if discounts appiled , then it also
            var final_orderline_price = price_without_discount - (price_without_discount * line_discount/100)
            console.log("discounted_price",final_orderline_price)
            //iterate through category
            product_categories.forEach((category_id) => {
                var category_id = category_id.id;
                console.log("categ name",category_id)
                // If the category doesn't exist in the dictionary, initialize it
                if (!categoryDiscounts[category_id]) {
                    categoryDiscounts[category_id] = {
                        category_name: category_id,
                        total_discounted_price: 0,
                        total_original_price:0
                    };
                }
                 // Add the total cost and actual price of this product to the corresponding category
                categoryDiscounts[category_id].total_discounted_price += final_orderline_price;
                categoryDiscounts[category_id].total_original_price += price_without_discount;

                console.log("categoryDiscounts",categoryDiscounts)
                // Object { 1: {…}, 2: {…}, 3: {…} }
                console.log("categoryDiscounts",categoryDiscounts[category_id])
                // Object { category_name: undefined, total_discounted_price: 207.86999999999998,
                // total_original_price: 277.15999999999997 }
            });
            for (var category_id in categoryDiscounts) {
                const CategoryId = categoryDiscounts[category_id]
                totalDiscountedPrice = CategoryId.total_discounted_price
                totalOriginalPrice = CategoryId.total_original_price
                const category = CategoryId.category_name;
                console.log("category",category)

                const discountType = category.discount_type;
                console.log('discountType',discountType)
                var PosCategory = this.models["pos.category"].getFirst();
                console.log("PosCategory",PosCategory)
//                var heloo = PosCategory.discount_type
//                console.log("heloo",heloo)
            }

        });
//        iterate over categoryDiscount dict to access total discount price and original price
//        then compare it with allowed price

//        for (var category_id in categoryDiscounts) {
//            const CategoryId = categoryDiscounts[category_id]
////            console.log("current_discount_total",totalDiscountedPrice)
//            totalDiscountedPrice = CategoryId.total_discounted_price
//            totalOriginalPrice = CategoryId.total_original_price
//            const category = CategoryId.category_name;
//            console.log("category",category)
//
//            var PosCategory = this.models["pos.category"].pos_categ_ids;
//            console.log("PosCategory",PosCategory)
//            var FixedDiscountLimit = this.models["pos.category"].getFirst().fixed_discount
//            console.log("PosCategory1",FixedDiscountLimit)
//            console.log("this",this)
//            const discountType = product_categories.discount_type;
//            console.log("discountType",discountType)
//            const FixedDiscountLimit = product_categories.fixed_discount;
//            console.log("FixedDiscountLimit",FixedDiscountLimit)
//            const PercentageDiscountLimit = product_categories.percent_discount;
//            console.log("PercentageDiscountLimit",PercentageDiscountLimit)
//
//
//            console.log("total_discount_total",totalDiscountedPrice)
//            console.log("current_pricet_total",totalOriginalPrice)
//            if (discount_type == 'fixed') {
//                var AllowedDiscount = totalOriginalPrice - FixedDiscountLimit
//                console.log("AllowedDiscount",AllowedDiscount)
//                if (AllowedDiscount < totalDiscountedPrice) {
//                    console.log('error')
//                };
//            }
//            else if (discount_type == 'percent_discount') {
//                var AllowedDiscount = totalOriginalPrice - (totalOriginalPrice * PercentageDiscountLimit)/100
//                console.log("AllowedDiscount",AllowedDiscount)
//                if (AllowedDiscount < totalDiscountedPrice) {
//                    console.log('error')
//                };
//            }

//        }
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
//            elif (category_id in categoryDiscounts){
//                };      var applied_discount_percent = (applied_discount / total_unit_price) * 100;
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





