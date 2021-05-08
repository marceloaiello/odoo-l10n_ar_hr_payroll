# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class ModuleName(models.Model):
    _inherit = 'hr.contract'
    antiquity_date = fields.Date(string='Fecha de Antiguedad')
    antiquity = fields.Integer(string="Antiguedad", readonly=True, compute="_compute_antiquity")

    @api.multi
    @api.depends('antiquity_date')
    def _compute_antiquity(self):
        for record in self:
            antiquity = 
            if record.antiquity_date:
                antiquity = relativedelta(
                    fields.Date.today(),
                    record.antiquity_date,
                ).years
            record.antiquity = antiquity

    @api.model
    def create(self, values):
        if not values.get('antiquity_date')
            values[:antiquity_date] = self.date_start
        return super().create(values)

