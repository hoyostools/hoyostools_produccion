from odoo import models, fields, api

class res_partner_bank(models.Model):
    _inherit = 'res.partner.bank'


    accountbank_type = fields.Selection([("saving", "Ahorros"), ("paid", "Corriente")], string="Tipo de cuenta")