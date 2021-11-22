# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class HrFiscalyearGroup(models.Model):
    _name = 'hr.fiscalyear.group'
    _description = 'Hr Fiscalyear Group'

    name = fields.Char(string='Periodo Fiscal')
    company_id = fields.Many2one('res.company', string='Empresa')
    period_ids = fields.One2many(
        'hr.period', 'hr_period_group_id', string='Periodos Asociados')
    payslip_ids = fields.One2many(
        'hr.payslip', string='Liquidaciones Vinculadas', related='period_ids.payslip_ids')
    suss_item_ids = fields.One2many(
        'hr.suss.item', 'period_group_id', string='AFIP - SUSS')

    def compute_suss(self):
        """
        Computes and returns a list of employees and the corresponding values for the
        selected periods of the period group.
        It helps building the table XXX which is used to generate sicoss txts and
        to show the data for the 931 DDJJ.
        """
        for employee in self.payslip_ids.mapped('employee_id'):
            self._create_suss_entry(employee.id, self.payslip_ids.filtered(
                lambda r: r.employee_id.id == employee.id))

    @api.model
    def _create_suss_entry(self, employee_id, payslips):
        self.ensure_one()
        values = {}
        entry = values.setdefault(
            employee_id, {
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
            })
        for payslip in payslips:
            for line in payslip.details_by_salary_rule_category:
                # add 931 values to the struct
                if line.code == 'BASIC931':
                    entry['sueldo'] += line.total
                elif line.code == 'ADIC931':
                    entry['adicionales'] += line.total
                elif line.code == 'NOREM931':
                    entry['no_remunerativo'] += line.total
                elif line.code == 'EXT931':
                    entry['horas_extra'] += line.total
                elif line.code == 'PLUSZDESF931':
                    entry['plus_zona_desfavorable'] += line.total
                elif line.code == 'SAC931':
                    entry['sac'] += line.total
                elif line.code == 'VAC931':
                    entry['vacaciones'] += line.total
                elif line.code == 'PREM931':
                    entry['premios'] += line.total
                elif line.code == 'MATERN931':
                    entry['maternidad'] += line.total
                elif line.code == 'RECTREM931':
                    entry['rectificativa_remuneracion'] += line.total
                elif line.code == 'INCSAL931':
                    entry['incremento_salarial'] += line.total
                elif line.code == 'TGROSS':
                    entry['subtotal_bruto'] += line.total
                elif line.code == 'TNOREM':
                    entry['subtotal_no_remunerativo'] += line.total
                elif line.code == 'TDESC':
                    entry['subtotal_descuentos'] += line.total
                elif line.code == 'TNET':
                    entry['subtotal_neto'] += line.total
        self.suss_item_ids = values.values()
