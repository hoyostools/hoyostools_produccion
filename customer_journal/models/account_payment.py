# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date, formatLang


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends('payment_type')
    def _compute_available_journal_ids(self):
        if not self.env.user.has_group_restriction:
            super()._compute_available_journal_ids()
        else:
            for pay in self:
                pay.available_journal_ids = self.env.user.account_journal_ids