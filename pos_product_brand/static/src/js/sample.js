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
        console.log("PosCategory",PosCategory)
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
                var category = CategoryId.category_name;
                console.log("category",category)

                const discountType = category.discount_type;
                console.log('discountType',discountType)
                var PosCategory = this.models["pos.category"].getAll();
                console.log("PosCategory",PosCategory)
//                let poscate = PosCategory.find(cat => cat.id == category_id);
                var heloo = PosCategory.discount_type
                console.log("heloo",heloo)
                var demo = PosCategory[0]
                console.log("demo",demo)
                console.log("demo",demo.percent_discount)
                console.log("demo",demo.discount_type)

                const posCategoryArray = PosCategory; // Your array-like structure

                for (let i = 0; i < posCategoryArray.length; i++) {
                    var AllCategory = posCategoryArray[i];
                    console.log("xxx",AllCategory); // Access each PosCategory object here
                    console.log("xxdiscount",AllCategory.discount_type)
                    var discount_type = AllCategory.discount_type
                    var FixedDiscountLimit = AllCategory.fixed_discount
                    var PercentageDiscountLimit = AllCategory.percent_discount
                    console.log("FixedDiscountLimit",FixedDiscountLimit)
                    console.log("PercentageDiscountLimit",PercentageDiscountLimit)
                    if (category == AllCategory.id) {
                        console.log('existed category',category)
                        console.log('existed category2',AllCategory.id)
                        if (discount_type == 'fixed') {
                            var AllowedDiscount = totalOriginalPrice - FixedDiscountLimit
                            console.log("AllowedDiscount",AllowedDiscount)
                            console.log("totalOriginalPrice",totalOriginalPrice)
                            if (AllowedDiscount > totalDiscountedPrice) {
                                console.log('error')
                                this.dialog.add(AlertDialog, {
                                    title: ("Alert!"),
                                    body: ("Category discount exceeded the limit."),
                                });
                                return;
                            }
                            else {
                                super.pay();
                            }
                            console.log("totalDiscountedPrice",totalDiscountedPrice)
                            console.log("AllowedDiscount",AllowedDiscount)
                        }
                        else if (discount_type == 'percentage') {
                            var AllowedDiscount = totalOriginalPrice - (totalOriginalPrice * PercentageDiscountLimit)/100
                            console.log("AllowedDiscount",AllowedDiscount);
                            if (AllowedDiscount > totalDiscountedPrice) {
                                console.log('error');
                                this.dialog.add(AlertDialog, {
                                    title: ("Alert!"),
                                    body: ("Category discount exceeded the limit."),
                                });
                                return;
                            }
                            else {
                                super.pay();
                            }
                            console.log("AllowedDiscount",AllowedDiscount);
                            console.log("totalDiscountedPrice",totalDiscountedPrice);

                        }

                    };
                }
            }
        });
    }
});