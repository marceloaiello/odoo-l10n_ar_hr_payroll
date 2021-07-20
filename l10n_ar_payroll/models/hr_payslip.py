# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time
from odoo import models, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # add computation of overtime hours from hr_attendance to the worked_day_lines get method.
    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(date_from, time.min)
            day_to = datetime.combine(date_to, time.max)

            # compute overtime hours from hr_attendance
            overtime_work_data = self.employee_id._get_attendance_hours_in_timeframe(
                day_from, day_to
            )
            overtime_data = {
                "name": _("Horas Extra, pagadas al 150%"),
                "sequence": 2,
                "code": "OVT50",
                "number_of_days": overtime_work_data["overtime_hours"] / overtime_work_data["theorical_hours"],
                "number_of_hours": overtime_work_data["overtime_hours"],
                "contract_id": contract.id,
            }

        return super(HrPayslip, self).get_worked_day_lines.append(overtime_data)
