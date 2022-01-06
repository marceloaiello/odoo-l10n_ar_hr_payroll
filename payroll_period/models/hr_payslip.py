# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    hr_period_id = fields.Many2one('hr.period', string='Periodo', readonly=True, states={'draft': [('readonly', False)]})
    date_payment = fields.Date(string='Fecha de Pago')

    @api.constrains('hr_period_id', 'company_id')
    def _check_period_company(self):
        self.ensure_one()
        if self.hr_period_id:
            if self.hr_period_id.company_id != self.company_id:
                raise ValidationError(
                    "The company on the selected period must "
                    "be the same as the company on the "
                    "payslip."
                )
        return True

    @api.onchange('company_id', 'contract_id')
    def onchange_company_id(self):
        if self.company_id and self.contract_id:
            period = self.env['hr.period'].get_next_period(
                self.company_id.id, self.contract_id.schedule_pay)
            self.hr_period_id = period.id if period else False

    @api.onchange('hr_period_id')
    def onchange_hr_period_id(self):
        if self.hr_period_id:
            period = self.hr_period_id
            self.date_from = period.date_start
            self.date_to = period.date_stop
            self.date_payment = period.date_payment
        self.with_context(contract=True).onchange_employee()

    @api.onchange('payslip_run_id')
    def onchange_payslip_run_id(self):
        for record in self:
            if record.payslip_run_id:
                period = record.payslip_run_id.hr_period_id
                self.hr_period_id = period.id
                if period:
                    self.name = _('Salary Slip of %s for %s') % (
                        self.employee_id.name, period.name)
        return
