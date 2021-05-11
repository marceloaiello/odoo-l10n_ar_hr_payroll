# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrLaborUnion(models.Model):
    _name = 'hr.labor_union'
    _description = 'Union Laboral / Sindicatos'

    name = fields.Char(string='Name')
    sindicato = fields.Char(string='Sindicato')
    convenio = fields.Char(string='Codigo C.C.T / RAMA')
    cct_categories = fields.One2many(comodel_name='hr.labor_union.category',inverse_name='labor_union_id',
                                        string='Categorias C.C.T')
    cct_svco_values = fields.One2many(comodel_name='hr.labor_union.svco_value',inverse_name='labor_union_id',
                                        string='S.V.C.O / Seguro de Vida')
    svco_current_value = fields.Float(compute='_compute_svco_current_value', string='Valor Actual - SVCO')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    @api.depends('cct_svco_values')
    def _compute_svco_current_value(self):
        for record in self:
            svco_value = 0
            domain = [('labor_union_id','=',record.id),('from_date','<=',context_today()),('to_date','>=',context_today())]
        if self.cct_svco_values.search_count(domain) == 1:
            for svco in record.cct_svco_values.search_count(domain):
                svco_value = svco.value
        else:
            raise UserError("Existen mas de un valor de SVCO para el periodo seleccionado. Esto no deberia pasar, consulte al administrador.")
        record.svco_current_value = svco_value

