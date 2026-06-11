/** @odoo-module **/

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

// =========================
// POS ORDER
// =========================

patch(PosOrder.prototype, {

    export_for_printing(baseUrl, headerData) {

        const result = super.export_for_printing(...arguments);

        if (this.partner_id) {
            result.headerData.customer_name = this.partner_id.name;
            result.headerData.customer_address = this.partner_id.contact_address;
            result.headerData.customer_mobile = this.partner_id.mobile;
            result.headerData.customer_phone = this.partner_id.phone;
            result.headerData.customer_email = this.partner_id.email;
            result.headerData.customer_vat = this.partner_id.vat;
        }

        if (this.cufe) {
            result.headerData.cufe_cude = this.cufe;
        }

        if (this.img_cufe) {
            result.headerData.img_cufe = this.img_cufe;
        }

        return result;
    },

});

// =========================
// POS ORDER LINE
// =========================

patch(PosOrderline.prototype, {

    getDisplayData() {

        const result = super.getDisplayData(...arguments);

        result.default_code = this.product_id.default_code || "";

        return result;
    },

});