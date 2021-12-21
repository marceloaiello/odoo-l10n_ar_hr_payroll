# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import Warning as UserError
from .hr_fiscal_year import get_schedules


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    hr_period_id = fields.Many2one(
        'hr.period',
        string='Periodo',
        states={'close': [('readonly', True)]}
    )
    schedule_pay = fields.Selection(
        get_schedules,
        'Pago Planificado',
        states={'close': [('readonly', True)]}
    )

    @api.model
    @api.constrains('hr_period_id', 'company_id')
    def _check_period_company(self):
        for run in self:
            if run.hr_period_id:
                if run.hr_period_id.company_id != run.company_id:
                    raise UserError("The company on the selected period must "
                                    "be the same as the company on the  "
                                    "payslip batch.")
        return True

    @api.model
    @api.constrains('hr_period_id', 'schedule_pay')
    def _check_period_schedule(self):
        for run in self:
            if run.hr_period_id:
                if run.hr_period_id.schedule_pay != run.schedule_pay:
                    raise UserError("The schedule on the selected period must "
                                    "be the same as the schedule on the "
                                    "payslip batch.")
        return True

    @api.model
    def get_default_schedule(self, company_id):
        for record in self:
            company = self.env['res.company'].browse(company_id)
            fy_obj = self.env['hr.fiscalyear']
            fys = fy_obj.search([
                ('state', '=', 'open'),
                ('company_id', '=', company.id),
            ])
            return (
                fys[0].schedule_pay
                if len(fys) else 'monthly'
            )

    #@api.onchange('company_id', 'schedule_pay')
    #def onchange_company_id(self):
    #    self.ensure_one()
    #    super(HrPayslipRun, self).onchange_company_id()
    #    schedule_pay = (self.schedule_pay or self.get_default_schedule(self.company_id.id))
    #    if len(self.company_id) and schedule_pay:
    #        period = self.env['hr.period'].get_next_period(self.company_id.id, schedule_pay)
    #        self.hr_period_id = period.id if period else False

    @api.onchange('hr_period_id')
    def onchange_period_id(self):
        if len(self.hr_period_id):
            self.date_start = self.hr_period_id.date_start
            self.date_end = self.hr_period_id.date_stop
            self.date_payment = self.hr_period_id.date_payment
            self.schedule_pay = self.hr_period_id.schedule_pay

    @api.model
    @api.returns('hr.employee')
    def get_employees(self):
        res = super(HrPayslipRun, self).get_employees()
        return res.filtered(lambda e: e.contract_id.schedule_pay == self.schedule_pay)

    @api.model
    def get_payslip_employees_wizard(self):
        res = super(HrPayslipRun, self).get_payslip_employees_wizard()
        res['context']['default_schedule_pay'] = self.schedule_pay
        return res

    @api.model
    def close_payslip_run(self):
        for run in self:
            if next((p for p in run.slip_ids if p.state == 'draft'), False):
                raise UserError("El lote de liquidaciones %s aun contiene liquidaciones "
                                "no confirmadas." % (run.name))
        self.update_periods()
        return super(HrPayslipRun, self).close_payslip_run()

    @api.model
    def draft_payslip_run(self):
        for run in self:
            run.hr_period_id.button_re_open()
        return super(HrPayslipRun, self).draft_payslip_run()

    @api.model
    def update_periods(self):
        for run in self:
            period = run.hr_period_id
            if len(period):
                # Close the current period
                period.button_close()
                # Open the next period of the fiscal year
                fiscal_year = period.fiscalyear_id
                next_period = fiscal_year.search_period(
                    number=period.number + 1)
                if next_period:
                    next_period.button_open()
