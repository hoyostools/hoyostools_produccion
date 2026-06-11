from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    cufe = fields.Char(string="CUFE/CUDE", store=True)
    img_cufe = fields.Char(string="QR CUFE/CUDE", store=True)

    def _generate_pos_order_invoice(self):
        res = super()._generate_pos_order_invoice()
        self._compute_cufe()
        self._compute_img_cufe()
        return res

    def _compute_cufe(self):
        for order in self:
            cufe = ''
            move = order.account_move
            if move and move.dian_document_lines:
                cufe = move.dian_document_lines[0].cufe_cude
            order.cufe = cufe

    def _compute_img_cufe(self):
        for order in self:
            img_cufe = ''
            move = order.account_move
            if move and move.dian_document_lines:
                img_cufe = move.dian_document_lines[:1].qr_code_dian_img or ''
            order.img_cufe = img_cufe

    @api.model
    def get_dian_receipt_data(self, pos_reference):
        """Return DIAN data for a POS receipt.

        Called from the POS ReceiptScreen after the order has been pushed to
        the backend and the invoice/account.move has been generated.
        """
        order = self.search([('pos_reference', '=', pos_reference)], limit=1)
        if not order:
            return {'cufe': '', 'img_cufe': ''}

        order._compute_cufe()
        order._compute_img_cufe()
        return {
            'cufe': order.cufe or '',
            'img_cufe': order.img_cufe or '',
        }
