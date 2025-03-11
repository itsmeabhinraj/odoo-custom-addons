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
        var PosCategory = this.models["pos.category"].records || [];
        //iterate through orderlines
        orderlines.forEach((line) => {
            var product = line.get_product();
            var line_discount = line.get_discount();
            var unit_qty = line.get_quantity();
            var price_without_discount = line.getUnitDisplayPriceBeforeDiscount() * unit_qty;
            var price_subtotal = line.price_subtotal;
            var product_categories = product.pos_categ_ids;
            //final price of product after tax (if discounts appiled , then it also
            var final_orderline_price = price_without_discount - (price_without_discount * line_discount/100)
            //iterate through category
            product_categories.forEach((category_id) => {
                var category_id = category_id.id;
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
            });
            for (var category_id in categoryDiscounts) {
                const CategoryId = categoryDiscounts[category_id]
                totalDiscountedPrice = CategoryId.total_discounted_price
                totalOriginalPrice = CategoryId.total_original_price
                var category = CategoryId.category_name;
                const discountType = category.discount_type;
                var PosCategory = this.models["pos.category"].getAll();
                const posCategoryArray = PosCategory;
                for (let i = 0; i < posCategoryArray.length; i++) {
                    var AllCategory = posCategoryArray[i];
                    var discount_type = AllCategory.discount_type
                    var FixedDiscountLimit = AllCategory.fixed_discount
                    var PercentageDiscountLimit = AllCategory.percent_discount
                    if (category == AllCategory.id) {
                        if (discount_type == 'fixed') {
                            var AllowedDiscount = totalOriginalPrice - FixedDiscountLimit
                            if (AllowedDiscount > totalDiscountedPrice) {
                                this.dialog.add(AlertDialog, {
                                    title: ("Alert!"),
                                    body: ("Category discount exceeded the limit."),
                                });
                                return;
                            }
                            else {
                                super.pay();
                            }
                        }
                        else if (discount_type == 'percentage') {
                            var AllowedDiscount = totalOriginalPrice - (totalOriginalPrice * PercentageDiscountLimit)/100
                            if (AllowedDiscount > totalDiscountedPrice) {
                                this.dialog.add(AlertDialog, {
                                    title: ("Alert!"),
                                    body: ("Category discount exceeded the limit."),
                                });
                                return;
                            }
                            else {
                                super.pay();
                            }
                        }

                    };
                }
            }
        });
    }
});
