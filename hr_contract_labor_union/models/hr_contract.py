# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'
    aplica_cct = fields.Boolean(string='Aplica C.C.T / Convenio?')
    cct_id = fields.Many2one(comodel_name='hr.labor_union', string='C.C.T / Sindicato')
    cct_category_id = fields.Many2one(comodel_name='hr.labor_union.category', string='Categoria C.C.T', onchange='on_change_cct_category_id')
    cct_value = fields.Monetary(name="Importe Categoria", readonly=True, options="{'currency_field': 'currency_id'}")
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)

    @api.depends('cct_category_id')
    @api.onchange(cct_category_id, aplica_cct)
    def on_change_cct_category_id(self):
        if self.cct_category_id:
            self.cct_value = self.cct_category_id.current_value
            self.amount = self.cct_category_id.current_value
        else:
            self.cct_value = 0
