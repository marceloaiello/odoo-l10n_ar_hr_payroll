# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time, timedelta
from num2words import num2words
from odoo import models, api, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def net_to_words_es(self, amount):
        return num2words(amount, to='currency', lang='es_CO')

    @api.model
    def ultimo_deposito_aportes(self):
        for record in self:
            slip_date = record.date_to
            last_month = slip_date.replace(day=1) - timedelta(days=1)
        return last_month

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        # Call super function computation and append new values.
        res = super().get_inputs(contracts, date_from, date_to)

        for contract in contracts:
            for advantage in contract.hr_contract_advantage_ids:
                res.append(
                    {
                        "name": advantage.contract_advantage_template_id.name,
                        "code": advantage.contract_advantage_template_id.code,
                        "contract_id": contract.id,
                        "amount": advantage.amount
                    }
                )
        return res

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(date_from, time.min)
            day_to = datetime.combine(date_to, time.max)
            work_hours_per_day = contract.resource_calendar_id.hours_per_day

            # -- compute public holidays leaves -- #
            # TODO: We take the public holidays from the model, so at some point we need to make sure to not pay the same days twice.
            ph_days = len(self.env["hr.holidays.public.line"].search(
                [('date', '>=', day_from), ('date', '<=', day_to)]))
            ph_hours = ph_days * work_hours_per_day
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
