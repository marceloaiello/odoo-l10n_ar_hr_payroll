# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class UpdatePricesWizard(models.TransientModel):
    _name = 'hr.labor_union.update_prices.wizard'
    _description = 'Hr Labor Union Category Prices Update - Wizard'

    update_prices_line_ids = fields.One2many(
        'hr.labor_union.update_prices.wizard.line', 'update_price_wzr', string='Importes')

    def update_wizard(self):
        vals = []
        for line in self.update_prices_line_ids.filtered(lambda r: r.is_changed):
            vals.append({
                'labor_union_category_id': line.labor_union_category_id.id,
                'from_date': line.from_date,
                'to_date': line.to_date,
                'value': line.amount,
                'company_id': line.company_id,
                'currency_id': line.currency_id,
            })

        self.env['hr.labor_union.category.price'].create(vals)


class UpdatePricesWizardLine(models.TransientModel):
    _name = 'hr.labor_union.update_prices.wizard.line'
    _description = 'Lines for Hr Labor Union Update Prices Wizard'

    update_price_wzr = fields.Many2one('hr.labor_union.update_prices.wizard')
    labor_union_category_id = fields.Many2one('hr.labor_union.category')
    from_date = fields.Date('Fecha Desde')
    to_date = fields.Date('Fecha Hasta')
    amount = fields.Float('Importe')
    is_changed = fields.Boolean(compute='_compute_is_changed', string="¿Con Cambios?", default=False)
    company_id = fields.Integer(string='Empresa')
    currency_id = fields.Integer(string='Moneda')

    @api.depends('amount')
    def _compute_is_changed(self):
        for rec in self:
            if rec.amount != rec.labor_union_category_id.current_value:
                rec.is_changed = True
            else:
                rec.is_changed = False
