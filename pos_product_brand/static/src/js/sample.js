import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        console.log(this.get_order());
        const order = this.get_order();
        const orderlines = order.get_orderlines();
        const categoryDiscounts = {}; // Store category-wise discounts

        for (const line of orderlines) {
            const product = line.get_product();
            const lineDiscount = line.get_discount();
            const productCategories = product.pos_categ_ids;
            const originalLinePrice = line.get_price_with_tax();
            const discountedLinePrice = line.price_subtotal;
            const actualDiscount = originalLinePrice - discountedLinePrice;

            for (const categoryId of productCategories) {
                const categoryObj = this.env.pos.db.get_category_by_id(categoryId);
                if (categoryObj && categoryObj.discount_limit && categoryObj.discount_type) {
                    if (!categoryDiscounts[categoryId]) {
                        categoryDiscounts[categoryId] = {
                            category: categoryObj,
                            totalDiscount: 0,
                            totalOriginal: 0,
                        };
                    }
                    categoryDiscounts[categoryId].totalDiscount += actualDiscount;
                    categoryDiscounts[categoryId].totalOriginal += originalLinePrice;
                }
            }
        }

        for (const categoryId in categoryDiscounts) {
            const categoryData = categoryDiscounts[categoryId];
            const category = categoryData.category;
            const totalDiscount = categoryData.totalDiscount;
            const totalOriginal = categoryData.totalOriginal;
            const discountLimit = category.discount_limit;
            const discountType = category.discount_type;

            if (discountType === 'percentage') {
                const maxAllowedDiscount = (totalOriginal * discountLimit) / 100;

                if (totalDiscount > maxAllowedDiscount) {
                    this.dialog.add(AlertDialog, {
                        title: _t("Warning"),
                        body: _t(Total discount (${totalDiscount.toFixed(2)}) exceeds the allowed limit (${discountLimit}%) for category: ${category.name}),
                    });
                    return; // Prevent payment
                }
            } else if (discountType === 'fixed') {
                if (totalDiscount > discountLimit) {
                    this.dialog.add(AlertDialog, {
                        title: _t("Warning"),
                        body: _t(Total discount (${totalDiscount.toFixed(2)}) exceeds the allowed limit (${discountLimit}) for category: ${category.name}),
                    });
                    return; // Prevent payment
                }
            }
        }

        return super.pay();
    },
});


import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

// Patch the PosStore to modify the payment logic
patch(PosStore.prototype, {
    async pay() {
        var orderlines = this.get_order().get_orderlines();
        var categoryDiscounts = {};
        var totalDiscountedPrice = 0;
        var totalOriginalPrice = 0;

        // Iterate through order lines to calculate discounts and prices
        orderlines.forEach((line) => {
            var categories = [];
            // Access categories of the product
            line.product_id.pos_categ_ids.forEach((category) => {
                categories.push(category.name);  // Push category names into array
            });
            console.log('Categories:', categories);
            console.log('Order lines:', orderlines);
            var product = line.get_product();
            console.log('Product:', product);

            // Get product discount - as percentage
            var line_discount = line.get_discount();
            console.log("Line discount:", line_discount);

            var unit_qty = line.get_quantity();
            console.log('Quantity:', unit_qty);

            // Price without discount
            var price_without_discount = line.getUnitDisplayPriceBeforeDiscount() * unit_qty;
            console.log('Price without discount:', price_without_discount);

            // Subtotal price of the order line
            var price_subtotal = line.price_subtotal;
            console.log('Price Subtotal:', price_subtotal);

            // Categories related to the product
            var product_categories = product.pos_categ_ids;
            console.log("Product Categories:", product_categories);

            // Final price of the order line after discount
            var final_orderline_price = price_without_discount - (price_without_discount * line_discount / 100);
            console.log("Discounted Price:", final_orderline_price);

            // Iterate through product categories
            product_categories.forEach((category) => {
                var category_id = category.id;  // Access the category ID
                var category_name = category.name;  // Access the category name
                console.log("Category ID:", category_id);
                console.log("Category Name:", category_name);

                // If the category doesn't exist in the dictionary, initialize it
                if (!categoryDiscounts[category_id]) {
                    categoryDiscounts[category_id] = {
                        category_name: category_name,  // Store the category name
                        total_discounted_price: 0,
                        total_original_price: 0,
                    };
                }

                // Add the discounted price and original price to the corresponding category
                categoryDiscounts[category_id].total_discounted_price +=
