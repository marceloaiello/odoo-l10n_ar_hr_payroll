# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'
    aplica_cct = fields.Boolean(string='Aplica C.C.T / Convenio?')
    cct_id = fields.Many2one(comodel_name='hr.labor_union', string='C.C.T / Sindicato')
    cct_category_id = fields.Many2one(comodel_name='hr.labor_union.category', string='Categoria C.C.T')

    @api.onchange("cct_category_id")
    def _onchange_cct_category_id(self):
        if self.cct_category_id is not None & self.aplica_cct == True:
            self.amount = self.cct_category_id.current_value
        else:
            self.amount = self.amount
