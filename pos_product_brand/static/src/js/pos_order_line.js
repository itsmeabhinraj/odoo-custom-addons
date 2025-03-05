import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";


patch(PosOrderline.prototype, {
    setup(vals) {
        this.product_brand = this.product_id.product_brand || "";
        return super.setup(...arguments);
    },
    getDisplayData() {
       return {
           ...super.getDisplayData(),
           product_brand: this.product_brand || "",
       };
    },
});
patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
           ...Orderline.props.line,
           shape: {
              ...Orderline.props.line.shape,
              product_brand: { type: String, optional: true },
           },
        },
    },
});