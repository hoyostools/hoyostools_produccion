from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    packaging_order_observation = fields.Char(
        string="Observación Empaque",
        readonly=True,
    )

    servicio_logistico = fields.Boolean(
        string="Servicio Logístico",
        readonly=True,
    )

    b4b = fields.Boolean(
        string="B4B",
        readonly=True,
    )

    notas_logisticas = fields.Char(
        string="Notas Logisticas",
        readonly=True,
    )

    def action_post(self):
        """
        Al confirmar una factura de proveedor:
        - Si existe payment_reference:
            coloca ese valor en el campo 'name' (Etiqueta)
            de todos los apuntes contables.
        - Si no existe:
            mantiene el comportamiento nativo de Odoo.
        """
        res = super().action_post()

        for move in self:
            # Solo facturas/proveedores
            if move.move_type in ("in_invoice", "in_refund"):
                if move.payment_reference:
                    move.line_ids.write({
                        "name": move.payment_reference
                    })

        return res

