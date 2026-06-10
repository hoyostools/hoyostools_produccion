from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"


    is_gift_adjustment_line = fields.Boolean(
        copy=False
    )