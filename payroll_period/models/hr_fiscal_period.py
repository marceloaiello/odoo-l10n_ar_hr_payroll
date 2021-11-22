# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from .hr_fiscal_year import get_schedules


class HrPeriod(models.Model):
    """
    PayrollFiscallPeriod adds the functionality of creating fiscal periods in which the diferent payslips can be
    grouped.
    """

    _name = 'hr.period'
    _description = 'Payroll Fiscalperiod'
    _order = 'date_start'

    name = fields.Char('Referencia', required=True, readonly=True, states={'draft': [('readonly', False)]})
    number = fields.Integer('Numero', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_start = fields.Date('Inicio del Periodo', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_stop = fields.Date('Fin del Periodo', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_payment = fields.Date('Fecha de Pago', required=True, readonly=True, states={'draft': [('readonly', False)]})
    fiscalyear_id = fields.Many2one('hr.fiscalyear', 'Año Fiscal', required=True, readonly=True, states={'draft': [('readonly', False)]}, ondelete='cascade')
    hr_period_group_id = fields.Many2one('hr.fiscalyear.group', 'Grupo del Periodo', readonly=True, states={'done': [('readonly', False)]})
    state = fields.Selection([('draft', 'Borrador'), ('open', 'Abierto'), ('done', 'Cerrado')], 'Estado', readonly=True, required=True, default='draft')
    company_id = fields.Many2one('res.company', string='Empresa', store=True, related="fiscalyear_id.company_id", readonly=True, states={'draft': [('readonly', False)]})
    schedule_pay = fields.Selection(get_schedules, 'Pago Planificado', required=True, readonly=True, states={'draft': [('readonly', False)]})
    payslip_ids = fields.One2many('hr.payslip', 'hr_period_id', 'Liquidaciones', readonly=True)

    @api.model
    def get_next_period(self, company_id, schedule_pay):
        """
         Get the next payroll period to process
        :rtype: hr.period browse record
        """
        periods = self.search([
            ('company_id', '=', company_id),
            ('schedule_pay', '=', schedule_pay),
            ('state', '=', 'open'),
        ], order='date_start', limit=1)

        return periods[0] if len(periods) else False

    @api.model
    def button_set_to_draft(self):
        for record in self:
            for period in self:
                if period.payslip_ids:
                    raise UserError(
                        _('You can not set to draft a period that already '
                            'has payslips computed'))
            record.write({'state': 'draft'})

    def button_open(self):
        for record in self:
            record.write({'state': 'open'})

    def button_close(self):
        for record in self:
            record.write({'state': 'done'})
            for period in record:
                fy = period.fiscalyear_id

                # If all periods are closed, close the fiscal year
                if all(p.state == 'done' for p in fy.period_ids):
                    fy.write({'state': 'done'})

    def button_re_open(self):
        for record in self:
            record.write({'state': 'open'})

            for period in record:
                fy = period.fiscalyear_id
                if fy.state != 'open':
                    fy.write({'state': 'open'})

