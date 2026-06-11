from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    cufe = fields.Char(string="CUFE/CUDE", store=True)
    img_cufe = fields.Char(string="CUFE/CUDE", store=True)

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
                img_cufe = move.dian_document_lines[0].qr_code_dian_img
            order.img_cufe = img_cufe