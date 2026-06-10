from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def _prepare_invoice_line(self, **optional_values):
        """
        Ensure reward gift products are invoiced without discount.
        Negative adjustment line is created later in account.move logic.
        """

        self.ensure_one()

        vals = super()._prepare_invoice_line(**optional_values)

        if (
            self.product_id
            and self.product_id.product_tmpl_id.producto_regalo
            and self.reward_id
        ):
            vals["discount"] = 0

        return vals