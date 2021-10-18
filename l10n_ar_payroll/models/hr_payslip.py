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

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        """
        Here we override the get_inputs function to add some computed inputs values
        (which might be editable then if the calculation is not ok.)
        """
        res = []

        structure_ids = contracts.get_all_structures()
        rule_ids = (
            self.env["hr.payroll.structure"].browse(structure_ids).get_all_rules()
        )
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        payslip_inputs = (
            self.env["hr.salary.rule"].browse(sorted_rule_ids).mapped("input_ids")
        )

        for contract in contracts:
            for payslip_input in payslip_inputs:
                res.append(
                    {
                        "name": payslip_input.name,
                        "code": payslip_input.code,
                        "contract_id": contract.id,
                        "amount": 0.00
                    }
                )
        return res

    @api.model
    def _compute_sac_input(self):
        """
        Calculo de mejor sueldo para Base de Calculo del SAC (Aguinaldo).
        El mejor sueldo debe ser calculado sobre los sueldos del ultimo periodo de 6 meses
        dependiendo del semestre en que se encuentre.
        (enero-junio / julio-diciembre).
        """


