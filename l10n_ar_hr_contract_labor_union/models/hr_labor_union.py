# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import api, fields, models, _


class HrLaborUnion(models.Model):
    _name = 'hr.labor_union'
    _inherit = 'mail.thread'
    _description = 'Union Laboral / Sindicatos'

    name = fields.Char(string='C.C.T / Sindicato', compute='_compute_name')
    sindicato = fields.Char(string='Sindicato')
    convenio = fields.Char(string='Codigo C.C.T / RAMA')
    cct_categories = fields.One2many(comodel_name='hr.labor_union.category',
                                     inverse_name='labor_union_id', string='Categorias C.C.T')
    cct_svco_values = fields.One2many(comodel_name='hr.labor_union.svco_value',
                                      inverse_name='labor_union_id', string=' CCT SVCO')
    svco_current_value = fields.Monetary(compute='_compute_svco_current_value',
                                         string='Valor Actual (SVCO)', options="{'currency_field': 'currency_id'}")
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Empresa',
                                 required=True, default=lambda self: self.env.user.company_id)

    @api.depends("sindicato", "convenio")
    def _compute_name(self):
        for record in self:
            if record.sindicato and record.convenio:
                record.name = "( " + record.convenio + " ) " + record.sindicato
            else:
                record.name = 'Nuevo sindicato / conveio...'

    @api.depends('cct_svco_values')
    def _compute_svco_current_value(self):
        for record in self:
            today = fields.Date.context_today(self).strftime('%Y-%m-%d')
            svco_value = 0.00
            domain = [('labor_union_id', '=', record.id),
                      ('from_date', '<=', today), ('to_date', '>=', today)]
            if record.cct_svco_values.search_count(domain) == 1:
                for svco in record.cct_svco_values.search(domain):
                    svco_value = svco.value
            record.svco_current_value = svco_value

    def action_update_wizard(self):
        lines = []
        for category in self.cct_categories:
            lines.append({
                'labor_union_category_id': category.id,
                'from_date': datetime.today(),
                'amount': category.current_value,
                'company_id': category.company_id.id,
                'currency_id': category.currency_id.id
            })
        return {'type': 'ir.actions.act_window',
                'name': _('Actualizar Importes'),
                'res_model': 'hr.labor_union.update_prices.wizard',
                'target': 'new',
                'view_id': self.env.ref('l10n_ar_hr_contract_labor_union.hr_labor_union_category_wizard').id,
                'view_mode': 'form',
                'context': {'default_update_prices_line_ids': lines}}
