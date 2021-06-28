# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    # Compute "Name" Based on formula so we dont need to input it manually
    @api.onchange("employee_id", "date_start")
    def _onchange_employee_date_start(self):
        if self.employee_id and self.date_start:
            self.name = "Contrato de: " + self.employee_id.name + \
                " de fecha: " + self.date_start.strftime("%d/%m/%Y")

    # Auto calculate end of trial period"
    @api.onchange('date_start')
    def _onchange_date_start(self):
        for record in self:
            if record.date_start:
                record.trial_date_end = record.date_start  # SUM MONTHS TODO:
