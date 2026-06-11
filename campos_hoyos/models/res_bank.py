from odoo import api, models, fields, _

class res_bank(models.Model):
    _inherit = 'res.bank'

    city_id = fields.Many2one('res.city', string='Ciudad')
    bank_code = fields.Char(string='Codigo Banco')
