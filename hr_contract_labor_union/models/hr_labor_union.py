# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrLaborUnion(models.Model):
    _name = 'hr.labor_union'
    _inherit = 'mail.thread'
    _description = 'Union Laboral / Sindicatos'

    name = fields.Char(string='C.C.T / Sindicato', compute="_compute_name")
    sindicato = fields.Char(string='Sindicato', track_visibility='onchange')
    convenio = fields.Char(string='Codigo C.C.T / RAMA', track_visibility='onchange')
    cct_categories = fields.One2many(comodel_name='hr.labor_union.category',inverse_name='labor_union_id',
                                        string='Categorias C.C.T', track_visibility='onchange')
    cct_svco_values = fields.One2many(comodel_name='hr.labor_union.svco_value',inverse_name='labor_union_id',
                                        string=' CCT SVCO', track_visibility='onchange')
    svco_current_value = fields.Monetary(compute='_compute_svco_current_value', string='Valor Actual (SVCO)')
    company_id = fields.Many2one('res.company', string='Empresa', required=True,
        default=lambda self: self.env.user.company_id)

    @api.depends('sindicato', 'convenio')
    def _compute_name(self):
        for record in self:
            record.name = "( " + record.convenio + " ) " + record.sindicato

    @api.depends('cct_svco_values')
    def _compute_svco_current_value(self):
        for record in self:
            today = fields.Date.context_today(self).strftime('%Y-%m-%d')
            svco_value = 0
            domain = [('labor_union_id', '=', record.id), ('from_date', '<=', today), ('to_date','>=',today)]
            if record.cct_svco_values.search_count(domain) == 1:
                for svco in record.cct_svco_values.search(domain):
                    svco_value = svco.value
            record.svco_current_value = svco_value

