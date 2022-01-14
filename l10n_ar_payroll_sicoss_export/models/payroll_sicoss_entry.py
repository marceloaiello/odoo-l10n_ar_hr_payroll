# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError


class PayrollSicossEntry(models.Model):
    _name = 'payroll.sicoss_entry'
    _description = 'Payroll Sicoss Entry'

    concept_mappings = {
        'BASIC931': 'sueldo',
        'ADIC931': 'adicionales',
        'NOREM931': 'no_remunerativo',
        'EXT931': 'horas_extra',
        'PLUSZDESF931': 'plus_zona_desfavorable',
        'SAC931': 'sac',
        'VAC931': 'vacaciones',
        'PREM931': 'premios',
        'MATERN931': 'maternidad',
        'RECTREM931': 'rectificativa_remuneracion',
        'INCSAL931': 'incremento_salarial',
        'TGROSS': 'subtotal_bruto',
        'TNOREM': 'subtotal_no_remunerativo',
        'TDESC': 'subtotal_descuentos',
        'TNET': 'subtotal_neto'
    }

    name = fields.Char(compute='_compute_name', string='Periodo Fiscal', store=True)
    year = fields.Integer(string='Año', required=True, readonly=True, states={'draft': [('readonly', False)]})
    month = fields.Selection([
        ('1', '01. Enero'),
        ('2', '02. Febrero'),
        ('3', '03. Marzo'),
        ('4', '04. Abril'),
        ('5', '05. Mayo'),
        ('6', '06. Junio'),
        ('7', '07. Julio'),
        ('8', '08. Agosto'),
        ('9', '09. Septiembre'),
        ('10', '10. Octubre'),
        ('11', '11. Noviembre'),
        ('12', '12. Diciembre')
    ], string='Mes', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approve', 'Aprobada'),
        ('closed', 'Enviada'),
        ('rejected', 'Rechazada')
    ], default='draft')
    payroll_sicoss_entry_item_ids = fields.One2many('payroll.sicoss_entry.item', 'sicoss_entry_id', string='Liquidacion - por empleado')
    period_ids = fields.One2many('hr.period', 'sicoss_entry_id', string='Liquidacion AFIP-SICOSS')

    @api.depends('year', 'month')
    def _compute_name(self):
        for record in self:
            if record.year and record.month:
                record.name = 'Liquidacion AFIP-SUSS periodo: ' + str(record.year) + '-' + str(record.month)

    @api.model
    def _create_suss_entry_item(self, employee_id, payslips):
        """
        Creates a Suss Entry Item from the passed employee_id and payslips.
        """
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
                if line.category_id.code in self.concept_mappings:
                    values[self.concept_mappings.get(line.category_id.code)] += line.total
        self.write({'payroll_sicoss_entry_item_ids': [(0, 0, values)]})

    def action_compute_suss(self):
        self.save()
        for sicoss_item in self.payroll_sicoss_entry_item_ids:
            sicoss_item.unlink()
        payslips = self.env['hr.period'].search([
            ('year', '=', self.year),
            ('month', '=', self.month),
            ('state', '=', 'done')
        ]).payslip_ids
        for employee in payslips.mapped('employee_id'):
            self._create_suss_entry_item(employee.id, payslips.filtered(lambda r: r.employee_id == employee))
        # self.write({'period_ids': [(0, 0, payslips.mapped('hr_period_id').values())]})

    def button_approve(self):
        for record in self:
            record.write({'state': 'approve'})

    def button_reject(self):
        for record in self:
            record.write({'state': 'rejected'})

    def button_close(self):
        for record in self:
            if record.state != 'approve':
                raise UserError('La liquidacion neceista ser aprobada antes de poder cerrarse.')
            record.write({'state': 'closed'})

    def button_set_to_draft(self):
        for record in self:
            if record.state == 'closed':
                raise UserError('No puedes volver a borrador una liquidacion que ya fue enviada y contabilizada.')
            record.write({'state': 'draft'})

    @api.constrains('year', 'month')
    def _check_unique_entries(self):
        for record in self:
            if self.env['payroll.sicoss_entry'].search_count([('year', '=', record.year), ('month', '=', record.month)]) > 0:
                raise ValidationError("Ya existe una declaracion jurada existente para el periodo seleccionado.")
