# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time

from odoo import models, api, _
from num2words import num2words


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def net_to_words_es(self, amount):
        return num2words(amount, lang='es')

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(date_from, time.min)
            day_to = datetime.combine(date_to, time.max)
            wkr_hours = contract.employee_id._get_work_days_data(day_from, day_to, calendar=contract.resource_calendar_id).number_of_hours

            # -- compute public holidays leaves -- #
            #
            # TODO: We take the public holidays from the model, so at some point we need to make sure to not pay the same days twice.
            ph_days = len(self.env["hr.holidays.public.line"].search([('date', '>=', day_from), ('date', '<=', day_to)]))
            ph_hours = ph_days * wkr_hours
            public_holidays_leaves = {
                "name": _("Feriados y No Laborables"),
                "sequence": 10,
                "code": "HFRD",
                "number_of_days": ph_days,
                "number_of_hours": ph_hours,
                "contract_id": contract.id,
            }

            # -- TODO: compute overtime -- #
            """
            overtimes = {}
            calendar = contract.resource_calendar_id
            overtime_intervals = []

            for day, hours, ovt in overtime_intervals:
                overtime = ovt[:1].overtime_id
                current_leave_struct = overtimes.setdefault(
                    overtime.holiday_status_id,
                    {
                        "name": overtime.holiday_status_id.name or _("Global Overtimes"),
                        "sequence": 5,
                        "code": overtime.holiday_status_id.code or "GLOBAL OVERTIMES",
                        "number_of_days": 0.0,
                        "number_of_hours": 0.0,
                        "contract_id": contract.id,
                    },
                )
                current_leave_struct["number_of_hours"] += hours
                if wkr_hours:
                    current_leave_struct["number_of_days"] += hours / wkr_hours
            """

        # Call super function computation and append new values.
        res = super().get_worked_day_lines(contracts, date_from, date_to)
        res.append(public_holidays_leaves)

        return res
