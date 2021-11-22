# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    employee_benefit_ids = fields.Many2many(
        'hr.employee.benefit.category',
        'salary_rule_employee_benefit_rel',
        'salary_rule_id', 'benefit_id', 'Salary Rules',
    )

    sum_all_benefits = fields.Boolean(
        'Include All Employee Benefits',
        default=True,
        help="If checked, the salary rule will sum over all employee "
        "benefits.",
    )

    def sum_benefits(self, payslip, **kwargs):
        """
        Method used to sum the employee benefits computed on the payslip

        Because there are many possible parameters and that the module
        needs to be inherited easily, arguments are passed through kwargs

        :param codes: The type of benefit over which to sum
        :type codes: list of string or single string

        :param employer: If True, sum over the employer contribution.
        If False, sum over the employee contribution

        Exemple
        -------
        payslip.compute_benefits(payslip, employer=True)
        Will return the employer contribution for the pay period
        """
        self.ensure_one()
        benefits = self._filter_benefits(payslip, **kwargs)
        employer = kwargs.get('employer', False)
        if employer:
            res = sum(ben.employer_amount for ben in benefits)
        else:
            res = sum(ben.employee_amount for ben in benefits)
        return res

    def _filter_benefits(self, payslip, codes=False, **kwargs):
        """ Filter the benefit records on the payslip
        :rtype: record set of hr.payslip.benefit.line
        """
        self.ensure_one()
        benefits = payslip.benefit_line_ids
        if codes:
            if isinstance(codes, str):
                codes = [codes]

            return benefits.filtered(
                lambda b: b.category_id.code in codes)

        if not self.sum_all_benefits:
            return benefits.filtered(
                lambda b: b.category_id in self.employee_benefit_ids)

        return benefits
