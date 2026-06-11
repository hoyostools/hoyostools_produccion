/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";

//Patching PaymentScreen
patch(PaymentScreen.prototype, {
      setup() {
        super.setup();
        this.orm = useService("orm");
        this.pos = usePos();
      },
    async validateOrder(isForceValidate) {

    var receipt_number = this.pos.selectedOrder.name;
    const data = this.env.services.pos.session_orders;
    var length = data.length - 1;
    var lastOrder = data[length];

    this.pos.customer_details = lastOrder.customer_details;
    this.pos.mobile = lastOrder.customer_mobile;
    this.pos.phone = lastOrder.customer_phone;
    this.pos.email = lastOrder.customer_email;
    this.pos.vat = lastOrder.customer_vat;
    this.pos.address = lastOrder.customer_address;
    this.pos.name = lastOrder.customer_name;
    const receipt_order = await super.validateOrder(isForceValidate);

    return receipt_order;
}
});
