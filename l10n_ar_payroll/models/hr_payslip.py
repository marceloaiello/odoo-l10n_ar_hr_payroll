# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time, timedelta
from pytz import timezone
from num2words import num2words
from odoo import models, api, _
from odoo.exceptions import ValidationError


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
                            "amount": 0.00
                        })
                current_overtime_struct['amount'] += overtime.units * overtime.overtime_type_id.fixed_amount
            res.extend(overtimes.values())

            # -- add sac inputs -- #
            if self._check_sac_period_valid(date_from):
                sac_base = {
                    "name": 'Mejor salario bruto mensual semestral - S.A.C',
                    "code": 'SACBASE',
                    "contract_id": contract.id,
                    "amount": self._get_max_salary_sac(contract, date_from).get('max_sum')
                }
                res.append(sac_base)

        return res

    def _check_sac_period_valid(self, date):
        if date.month == 6 or date.month == 12:
            return True
        else:
            return False

    def _get_sac_semester(self, date):
        sac_semester = {'sac_year': date.year, 'sac_months': []}
        if date.month == 6:
            sac_semester['sac_months'] = [1, 2, 3, 4, 5]
        elif date.month == 12:
            sac_semester['sac_months'] = [7, 8, 9, 10, 11]
        return sac_semester

    def _get_max_salary_sac(self, contract, date_from):
        if not self._check_sac_period_valid(date_from):
            raise ValidationError('ERROR. No esta liquidando un periodo adecuado para el S.A.C. Verifique las fechas.')
        sac_semester = self._get_sac_semester(date_from)
        data = self.env['payroll.sicoss_entry'].search([
            ('year', '=', sac_semester.get('sac_year')),
            ('month', 'in', sac_semester.get('sac_months')),
        ]).payroll_sicoss_entry_item_ids.filtered(lambda r: r.employee_id == contract.employee_id)
        sac_data = {'max_period': 'N/a', 'max_sum': 0.00}
        for period in data:
            sum = period.sueldo + period.adicionales + period.horas_extra
            if sum > sac_data["max_sum"]:
                sac_data["max_period"] = str(period.sicoss_entry_id.year) + '-' + str(period.sicoss_entry_id.month)
                sac_data["max_sum"] = sum

        return sac_data

    def get_full_work_days_month(self, contract, date_from, date_to):
        res = contract.employee_id._get_work_days_data(
            datetime.combine(date_from.replace(day=1), datetime.min.time()),
            datetime.combine(date_to, datetime.max.time()),
            calendar=contract.resource_calendar_id,
            compute_leaves=False)["days"]
        return res

    def get_real_work_days_month(self, contract, date_from, date_to):
        res = contract.employee_id._get_work_days_data(
            datetime.combine(date_from.replace(day=1), datetime.min.time()),
            datetime.combine(date_to, datetime.max.time()),
            calendar=contract.resource_calendar_id,
            compute_leaves=True)["days"]
        return res

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        # We completely override this function because day calculations in Argentina are
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
            work_hours_per_day = 9  # FIXME: This is hardcoded, we have to find a method to return the correct hours.

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
            res.extend(leaves.values())

            # -- compute public holidays leaves -- #
            public_holidays = self.env['hr.holidays.public'].get_holidays_list(
                year=day_from.year, start_dt=day_from, end_dt=day_to, employee_id=contract.employee_id.id
            )
            ph_days = len(public_holidays)
            ph_hours = ph_days * work_hours_per_day
            public_holidays_leaves = {
                "name": _("Feriados y No Laborables"),
                "sequence": 2,
                "code": "HFRD",
                "number_of_days": ph_days,
                "number_of_hours": ph_hours,
                "contract_id": contract.id,
            }
            if ph_days != 0:
                res.append(public_holidays_leaves)

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
                "number_of_days": work_data["days"],
                "number_of_hours": work_data["hours"],
                "contract_id": contract.id,
            }
            res.append(attendances)

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
                    current_overtime_struct["number_of_hours"] += overtime.overtime_hours
                    current_overtime_struct["number_of_days"] += overtime.overtime_hours / work_hours_per_day
            res.extend(overtimes.values())

            # -- compute sac days -- #
            # FIXME: Los dias los esta calculando restando fines de semana. No deberia ser asi, sino que debe calcualr dias corridos,
            # las unicas ausencias que se deben descontar son las de ausentismos injustificados o licencias.
            # Por ende, esto si bien funciona, hay que pulir eso, y actualmente los dias deben editarse manualmanete en el S.A.C.
            if self._check_sac_period_valid(day_from):
                sac_semester = self._get_sac_semester(day_from)
                sac_from = datetime(sac_semester.get('sac_year'), sac_semester.get('sac_months')[0], 1)
                sac_to = datetime(sac_semester.get('sac_year'), sac_semester.get('sac_months')[-1] + 1, 1) - timedelta(days=1)
                sac_work_data = contract.employee_id._get_work_days_data(
                    datetime.combine(sac_from, time.min),
                    datetime.combine(sac_to, time.max),
                    calendar=contract.resource_calendar_id, compute_leaves=True)
                sac_data = {
                    "name": _("Dias trabajados en el semestre - S.A.C"),
                    "sequence": 90,
                    "code": "WORK100",
                    "number_of_days": sac_work_data["days"],
                    "number_of_hours": sac_work_data["hours"],
                    "contract_id": contract.id,
                }
                res.append(sac_data)

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
