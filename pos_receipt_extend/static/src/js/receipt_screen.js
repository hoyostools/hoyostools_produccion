/** @odoo-module **/

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { onWillStart } from "@odoo/owl";

patch(ReceiptScreen.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.pos = usePos();

        onWillStart(async () => {
            const order = this.pos.get_order();
            if (!order) {
                return;
            }

            const data = await this.orm.call(
                "pos.order",
                "get_dian_receipt_data",
                [order.name]
            );

            order.cufe = data.cufe || "";
            order.img_cufe = data.img_cufe || "";
        });
    },
});
