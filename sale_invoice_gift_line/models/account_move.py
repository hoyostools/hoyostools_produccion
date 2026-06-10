from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"


    @api.model_create_multi
    def create(self, vals_list):

        moves = super().create(vals_list)

        AccountMoveLine = self.env["account.move.line"]

        for move in moves:

            if move.move_type != "out_invoice":
                continue

            adjustment_lines = []

            for line in move.invoice_line_ids:

                sale_lines = line.sale_line_ids.filtered(
                    lambda l:
                        l.reward_id
                        and l.product_id.product_tmpl_id.producto_regalo
                )

                if not sale_lines:
                    if move.pos_order_ids:
                        linea = move.invoice_line_ids.filtered(
                            lambda l:
                            l.price_unit < 0
                            and l.product_id.product_tmpl_id.producto_regalo
                        )
                        if linea:
                            linea.write({'tax_ids': [(5, 0, 0)]})
                    continue


                adjustment_lines.append({
                    "move_id": move.id,
                    "product_id": line.product_id.id,
                    "name": f"{line.name} (Ajuste producto regalo)",
                    "quantity": line.quantity,
                    "price_unit": -line.price_unit,
                    "tax_ids": [],
                    "account_id": line.account_id.id,
                    "is_gift_adjustment_line": True,
                })

            if adjustment_lines:
                AccountMoveLine.create(adjustment_lines)

        return moves