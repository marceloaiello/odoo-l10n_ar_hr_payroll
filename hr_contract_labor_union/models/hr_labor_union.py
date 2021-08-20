# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class HrLaborUnion(models.Model):
    _name = 'hr.labor_union'
    _inherit = 'mail.thread'
    _description = 'Union Laboral / Sindicatos'

    name = fields.Char(string='C.C.T / Sindicato', compute='_compute_name')
    sindicato = fields.Char(string='Sindicato', track_visibility='onchange')
    convenio = fields.Char(string='Codigo C.C.T / RAMA', track_visibility='onchange')
    cct_categories = fields.One2many(comodel_name='hr.labor_union.category',
                                     inverse_name='labor_union_id', string='Categorias C.C.T', track_visibility='onchange')
    cct_svco_values = fields.One2many(comodel_name='hr.labor_union.svco_value',
                                      inverse_name='labor_union_id', string=' CCT SVCO', track_visibility='onchange')
    svco_current_value = fields.Monetary(compute='_compute_svco_current_value',
                                         string='Valor Actual (SVCO)', options="{'currency_field': 'currency_id'}")
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Empresa',
                                 required=True, default=lambda self: self.env.user.company_id)

    @api.depends("sindicato", "convenio")
    def _compute_name(self):
        if self.sindicato and self.convenio:
            self.name = "( " + self.convenio + " ) " + self.sindicato

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

    def define_prices_form(self):
        return {
            'name': "Definir Importes",
            'type': 'ir.actions.act_url',
            # The url is the same as above
            'url': "/web?&#action=276&model=hr.labor_union.category.price&view_type=list",
            'target': 'new'
        }

    def action_update_wizard(self): #TODO:
        category_ids = self.env['hr.labor_union.category'].browse(self._context.get('cct_categories', False))
        lines = []
        for line in category_ids:
            context = ({
                'labor_union_category_id': line.id,
                'from_date': fields.today(),
                'to_date': fields.today(),
                'amount': line.current_value,
            })
            lines.append(context)

        return {'type': 'ir.actions.act_window',
                'name': _('Update Prices'),
                'res_model': 'hr.labor_union.category.prices.wizard',
                'target': 'new',
                'view_id': self.env.ref('hr_contract_labor_union.hr_labor_union_category_wizard').id,
                'view_mode': 'form',
                'context': {'labor_union_category_ids': lines}}
