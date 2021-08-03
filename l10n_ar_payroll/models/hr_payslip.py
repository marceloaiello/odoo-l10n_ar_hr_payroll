# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time
from odoo import models, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        """
        In this inherited function we append the overtime structs to the
        original get_worked_day_lines response "res".
        """
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(date_from, time.min)
            day_to = datetime.combine(date_to, time.max)

            # -- compute overtime hours -- #
            overtimes = {}
            for overtime in self.env['hr.overtime'].search(
                [('employee_id' '=', contract.employee_id.id), ('state' '=' 'validate'),
                 ('start_date', '>=', day_from), ('start_date' '<=', day_to)]):
                current_overtime_struct = overtimes.setdefault(
                    overtime.overtime_type_id, {
                        "name": overtime.overtime_type_id.name or _("Horas Extras"),
                        "sequence": 10,
                        "code": overtime.overtime_type_id.code or "OVT50",
                        "number_of_days": 0.0,
                        "number_of_hours": 0.0,
                        "contract_id": contract.id,
                    },
                )
                current_overtime_struct["number_of_hours"] += overtime.overtime_hours

        # Call super function computation and append new values.
        res = super().get_worked_day_lines(contracts, date_from, date_to)
        res.extend(overtimes.values())

        return res
