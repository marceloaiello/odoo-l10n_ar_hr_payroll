# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class HrLaborUnionCategoryPricesWizard(models.TransientModel):
    _name = 'hr.labor_union.category.prices.wizard'
    _description = 'Hr Labor Union Category Prices Wizard'

    labor_union_category_id = fields.Many2one('hr.labor_union.category')
    from_date = fields.Date('Fecha Desde')
    to_date = fields.Date(string='Fecha Hasta')
    amount = fields.Float(string='Importe')
    # TODO: Hay que crear uno para los items... (
    # )

    @api.model
    def update_wizard(self):
        vals = []
        for item in self.labor_union_category_prices:
            record = {}
            record.setdefault({
                'labor_union_category_id': item.labor_union_category_id,
                'from_date': item.from_date,
                'to_date': item.to_date,
                'value': item.amount,
            })
            vals.append(record)

        self.env['hr.labor_union.category.prices'].create(vals)






