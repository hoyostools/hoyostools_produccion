/** @odoo-module **/

import { Order, Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

// =========================
// POS ORDER
// =========================

patch(Order.prototype, {

    export_for_printing() {

        const result = super.export_for_printing(...arguments);

        if (this.partner) {
            result.headerData.customer_name = this.partner.name;
            result.headerData.customer_address = this.partner.contact_address;
            result.headerData.customer_mobile = this.partner.mobile;
            result.headerData.customer_phone = this.partner.phone;
            result.headerData.customer_email = this.partner.email;
            result.headerData.customer_vat = this.partner.vat;
        }

        // These values are assigned from ReceiptScreen after the order
        // has been validated and saved in the backend.
        result.headerData.cufe_cude = this.cufe || "";
        result.headerData.img_cufe = this.img_cufe || "";

        return result;
    },

});

// =========================
// POS ORDER LINE
// =========================

patch(Orderline.prototype, {

    getDisplayData() {

        const result = super.getDisplayData(...arguments);

        result.default_code = this.product?.default_code || "";

        return result;
    },

});