# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    benefit_line_ids = fields.One2many(
        'hr.payslip.benefit.line',
        'payslip_id',
        'Employee Benefits',
        readonly=True, states={'draft': [('readonly', False)]},
        copy=True,
    )

    def _search_benefits(self):
        """
        Search employee benefits to be added on the payslip

        This method is meant to be inherited in other modules
        in order to add benefits from other sources.
        """
        self.ensure_one()
        return self.contract_id.benefit_line_ids

    def button_compute_benefits(self):
        self.compute_benefits()

    def compute_benefits(self):
        """
        Compute the employee benefits on the payslip.

        This method can be called from inside a salary rule.

        Exemple
        -------
        payslip.compute_benefits()

        This is required when the benefits are based on the value
        of one or more salary rules.

        The module hr_employee_benefit_percent implements that
        functionnality.
        """
        for benefit_line in self.benefit_line_ids:
            if benefit_line.source == 'contract':
                benefit_line.unlink()

        benefits = self._search_benefits()

        # Compute the amounts for each employee benefit
        benefits.compute_amounts(self)

        # If the method is called from a salary rule.
        # It is important to call refresh() so that the record set
        # will contain the benefits computed above.
        self.refresh()
