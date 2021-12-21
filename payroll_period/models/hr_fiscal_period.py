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
    afip_suss_item_ids = fields.One2many('hr.suss.item', 'period_id', string='AFIP - SUSS')

    @api.model
    def _create_suss_entry(self, employee_id, payslips):
        self.ensure_one()
        values = {
            'employee_id': employee_id,
            'sueldo': 0.00,
            'adicionales': 0.00,
            'horas_extra': 0.00,
            'plus_zona_desfavorable': 0.00,
            'sac': 0.00,
            'vacaciones': 0.00,
            'premios': 0.00,
            'no_remunerativo': 0.00,
            'maternidad': 0.00,
            'rectificativa_remuneracion': 0.00,
            'incremento_salarial': 0.00,
            'subtotal_bruto': 0.00,
            'subtotal_no_remunerativo': 0.00,
            'subtotal_descuentos': 0.00,
            'subtotal_neto': 0.00,
        }
        for payslip in payslips:
            for line in payslip.details_by_salary_rule_category:
                # add 931 values to the struct
                if line.category_id.code == 'BASIC931':
                    values['sueldo'] += line.total
                elif line.category_id.code == 'ADIC931':
                    values['adicionales'] += line.total
                elif line.category_id.code == 'NOREM931':
                    values['no_remunerativo'] += line.total
                elif line.category_id.code == 'EXT931':
                    values['horas_extra'] += line.total
                elif line.category_id.code == 'PLUSZDESF931':
                    values['plus_zona_desfavorable'] += line.total
                elif line.category_id.code == 'SAC931':
                    values['sac'] += line.total
                elif line.category_id.code == 'VAC931':
                    values['vacaciones'] += line.total
                elif line.category_id.code == 'PREM931':
                    values['premios'] += line.total
                elif line.category_id.code == 'MATERN931':
                    values['maternidad'] += line.total
                elif line.category_id.code == 'RECTREM931':
                    values['rectificativa_remuneracion'] += line.total
                elif line.category_id.code == 'INCSAL931':
                    values['incremento_salarial'] += line.total
                elif line.category_id.code == 'TGROSS':
                    values['subtotal_bruto'] += line.total
                elif line.category_id.code == 'TNOREM':
                    values['subtotal_no_remunerativo'] += line.total
                elif line.category_id.code == 'TDESC':
                    values['subtotal_descuentos'] += line.total
                elif line.category_id.code == 'TNET':
                    values['subtotal_neto'] += line.total

        self.write({'afip_suss_item_ids': [(0, 0, values)]})

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
            record.action_compute_suss()
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

    def action_compute_suss(self):
        """
        Computes and returns a list of employees and the corresponding values for the
        selected periods of the period group.
        It helps building the table XXX which is used to generate sicoss txts and
        to show the data for the 931 DDJJ.
        """
        for suss_item in self.afip_suss_item_ids:
            suss_item.unlink()
        for employee in self.payslip_ids.mapped('employee_id'):
            self._create_suss_entry(employee.id, self.payslip_ids.filtered(lambda r: r.employee_id == employee))

