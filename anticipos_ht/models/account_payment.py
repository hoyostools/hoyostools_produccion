from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    tipo_anticipo_id = fields.Many2one(
        "ap.anticipo",
        string="Tipo de anticipo"
    )

    anticipo = fields.Boolean(
        string="Anticipo"
    )

    voucher_type = fields.Selection([
        ('pago', 'Pago'),
        ('anticipo', 'Anticipo')
    ], string='Tipo de Pago')

    @api.onchange('voucher_type')
    def _onchange_voucher_type(self):
        if self.voucher_type != 'anticipo':
            self.tipo_anticipo_id = False

    @api.onchange('tipo_anticipo_id')
    def _onchange_tipo_anticipo_id(self):
        if self.tipo_anticipo_id:
            self.destination_account_id = self.tipo_anticipo_id.cuenta_anticipo_id

    def _prepare_move_line_default_vals(
        self,
        write_off_line_vals=None,
        force_balance=False
    ):
        vals_list = super()._prepare_move_line_default_vals(
            write_off_line_vals,
            force_balance=force_balance
        )

        if (
            self.voucher_type == 'anticipo'
            and self.tipo_anticipo_id
            and self.tipo_anticipo_id.cuenta_anticipo_id
        ):
            account = self.tipo_anticipo_id.cuenta_anticipo_id

            for vals in vals_list:
                account = self.env['account.account'].browse(
                    vals['account_id']
                )

                if account.account_type in (
                    'asset_receivable',
                    'liability_payable'
                ):
                    vals['account_id'] = self.tipo_anticipo_id.cuenta_anticipo_id.id

        return vals_list