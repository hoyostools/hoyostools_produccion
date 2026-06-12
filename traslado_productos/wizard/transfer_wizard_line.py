from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class StockTransferWizardLine(models.TransientModel):
    _name = 'stock.transfer.wizard.line'

    wizard_id = fields.Many2one('stock.transfer.wizard')

    product_id = fields.Many2one('product.product', readonly=True, store=True)
    location_id = fields.Many2one('stock.location', readonly=True)

    available_qty = fields.Float(string="Disponible", readonly=True)

    qty_to_move = fields.Float(string="Cantidad a trasladar", required=True)

    location_dest_id = fields.Many2one(
        'stock.location',
        string="Ubicación destino",
    )