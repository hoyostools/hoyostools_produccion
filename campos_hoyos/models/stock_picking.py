from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    address_complete = fields.Char(related='partner_id.street')
    carrier_id_name = fields.Char(related='carrier_id.name')
    packaging_order_observation = fields.Text(string='Totalidad del empaque de la orden', related='sale_id.packaging_order_observation', store=True, readonly=False,)
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        string="Almacén",
        related="picking_type_id.warehouse_id",
        store=True,
        readonly=True,
    )