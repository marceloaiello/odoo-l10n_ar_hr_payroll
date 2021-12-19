# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time, timedelta
from pytz import timezone
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

            # -- compute contract advantages -- #
            for advantage in contract.hr_contract_advantage_ids:
                res.append(
                    {
                        "name": advantage.contract_advantage_template_id.name,
                        "code": advantage.contract_advantage_template_id.code,
                        "contract_id": contract.id,
                        "amount": advantage.amount
                    }
                )

            # -- compute overtimes - fixed -- #
            overtimes = {}
            for overtime in self._get_overtime_data(contract, date_from, date_to):
                if overtime.overtime_type_id.duration_type == 'unit':
                    current_overtime_struct = overtimes.setdefault(
                        overtime.overtime_type_id, {
                            "name": overtime.overtime_type_id.name,
                            "code": overtime.overtime_type_id.payroll_code,
                            "contract_id": contract.id,
                            "amount": overtime.units
                        })
            res.extend(overtimes.values())

            # -- compute contract sac inputs if sac month  -- #
            if date_from.month == 6:
                # get the best gross payslip in the first 6 months of the year (1 semester)
                payslisp = contract.employee_id.payslip_ids.search(
                    [
                        ('date_from', '>=', 'TODO:')
                        ('date_to', '<=', 'TODO:')

                    ]
                )

                sac_base = {
                    "name": 'Base de calculo S.A.C',
                    "code": 'SACBASE',
                    "contract_id": contract.id,
                    "amount": "TODO:"
                }
                sac_days = {
                    "name": 'Base de calculo S.A.C',
                    "code": 'SACBASE',
                    "contract_id": contract.id,
                    "amount": "TODO:"
                }

            elif date_from.month == 12:

        return res

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        # We will completely override this function because day calculations in Argentina are
        # very diferent to the odoo day calculations.
        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be
        applied for the given contract between date_from and date_to
        """
        res = []
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(date_from, time.min)
            day_to = datetime.combine(date_to, time.max)
            work_hours_per_day = contract.resource_calendar_id.hours_per_day

            # -- compute leave days -- #
            leaves = {}
            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)
            day_leave_intervals = contract.employee_id.list_leaves(
                day_from, day_to, calendar=contract.resource_calendar_id
            )
            for day, hours, leave in day_leave_intervals:
                holiday = leave[:1].holiday_id
                current_leave_struct = leaves.setdefault(
                    holiday.holiday_status_id,
                    {
                        "name": holiday.holiday_status_id.name or _("Global Leaves"),
                        "sequence": 5,
                        "code": holiday.holiday_status_id.code or "GLOBAL",
                        "number_of_days": 0.0,
                        "number_of_hours": 0.0,
                        "contract_id": contract.id,
                    },
                )
                current_leave_struct["number_of_hours"] -= hours
                work_hours = calendar.get_work_hours_count(
                    tz.localize(datetime.combine(day, time.min)),
                    tz.localize(datetime.combine(day, time.max)),
                    compute_leaves=False,
                )
                if work_hours:
                    current_leave_struct["number_of_days"] -= hours / work_hours

            # -- compute public holidays leaves -- #
            ph_days = len(self.env["hr.holidays.public.line"].search(
                [('date', '>=', day_from), ('date', '<=', day_to)]))
            ph_hours = ph_days * work_hours_per_day
            public_holidays_leaves = {
                "name": _("Feriados y No Laborables"),
                "sequence": 2,
                "code": "HFRD",
                "number_of_days": ph_days,
                "number_of_hours": ph_hours,
                "contract_id": contract.id,
            }
            # TODO: We take the public holidays from the model, so at some point we need
            # to make sure to not pay the same days twice.
            # Maybe we can do it with a boolean inheriting the public holidays model.

            # -- compute worked days (substracting the public holidays) -- #
            work_data = contract.employee_id._get_work_days_data(
                day_from, day_to, calendar=contract.resource_calendar_id, compute_leaves=False
            )
            attendances = {
                "name": _("Normal Working Days paid at 100%"),
                "sequence": 1,
                "code": "WORK100",
                "number_of_days": work_data["days"] - ph_days,
                "number_of_hours": work_data["hours"] - ph_hours,
                "contract_id": contract.id,
            }

            # -- compute overtimes -- #
            overtimes = {}
            for overtime in self._get_overtime_data(contract, day_from, day_to):
                if overtime.overtime_type_id.duration_type == 'hour':
                    current_overtime_struct = overtimes.setdefault(
                        overtime.overtime_type_id, {
                            "name": overtime.overtime_type_id.name or _("Global Overtimes"),
                            "sequence": 10,
                            "code": overtime.overtime_type_id.payroll_code or "GLOBALOVT",
                            "number_of_days": 0.0,
                            "number_of_hours": 0.0,
                            "contract_id": contract.id,
                        })
                    current_overtime_struct["number_of_hours"] = overtime.overtime_hours
                    current_overtime_struct["number_of_days"] = overtime.overtime_hours / 24

            res.append(attendances)
            res.extend(leaves.values())
            res.extend(overtimes.values())
            if ph_days != 0:
                res.append(public_holidays_leaves)
        return res

    def _get_overtime_data(self, contract, day_from, day_to):
        res = self.env['hr.overtime'].search(
            [
                ('employee_id', '=', contract.employee_id.id),
                ('state', '=', 'validate'),
                ('start_date', '>=', day_from), ('start_date', '<=', day_to),
            ]
        )
        return res
