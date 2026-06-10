import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        """Extiende la factura para manejar productos regalo como descuento"""
        invoice_vals = super()._prepare_invoice()

        new_invoice_lines = []

        for line in invoice_vals.get('invoice_line_ids', []):
            
            if isinstance(line, tuple) and line[0] == 0:
                vals = line[2]
                product_id = vals.get('product_id')
                product = self.env['product.product'].browse(product_id)
                is_gift = product.product_tmpl_id.producto_regalo

                if is_gift:
                    price = product.lst_price

                    negative_line = vals.copy()
                    negative_line.update({
                        'price_unit': -price,
                        'name': (vals.get('name') or '') + ' (Descuento Regalo)',
                    })

                    new_invoice_lines.append((0, 0, negative_line))
                else:
                    new_invoice_lines.append(line)

        invoice_vals['invoice_line_ids'] = new_invoice_lines

        return invoice_vals

    def _get_reward_values_product(self, reward, coupon, product=None, **kwargs):

        reward_vals_list = super()._get_reward_values_product(
            reward,
            coupon,
            product=product,
            **kwargs
        )

        reward_product = product or reward.reward_product_ids[:1]

        if not reward_product:
            return reward_vals_list

        if not reward_product.product_tmpl_id.producto_regalo:
            return reward_vals_list

        quantity = reward_vals_list[0].get("product_uom_qty", 1.0)

        # método correcto pricing engine Odoo 18
        price = self.pricelist_id._get_products_price(
            reward_product,
            quantity,
            partner=self.partner_id
        )[reward_product.id]

        for vals in reward_vals_list:
            vals["price_unit"] = price

        return reward_vals_list

    def _write_vals_from_reward_vals(self, reward_vals, old_lines, delete=True):
        self.ensure_one()

        protected_prices = {}
        for vals, line in zip(reward_vals, old_lines):
            if (
                line.product_id
                and line.product_id.product_tmpl_id.producto_regalo
                and line.reward_id
            ):
                protected_prices[line.id] = line.price_unit

        result = super()._write_vals_from_reward_vals(
            reward_vals,
            old_lines,
            delete=delete,
        )

        for vals, line in zip(reward_vals, old_lines):
            if (
                line.exists()
                and line.product_id
                and line.product_id.product_tmpl_id.producto_regalo
                and line.reward_id
            ):
                incoming_price = vals.get("price_unit")
                final_price = incoming_price if incoming_price is not None else protected_prices.get(line.id)

                if final_price is not None and line.price_unit != final_price:
                    line.price_unit = final_price

                _logger.warning(
                    "GIFT REWARD _write_vals_from_reward_vals order=%s line=%s product=%s incoming_price=%s final_line_price=%s vals=%s",
                    self.name,
                    line.id,
                    line.product_id.display_name,
                    incoming_price,
                    line.price_unit,
                    vals,
                )

        return result