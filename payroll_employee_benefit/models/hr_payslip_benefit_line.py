# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _
from odoo.addons import decimal_precision as dp


class HrPayslipBenefitLine(models.Model):
    """Pay Slip Employee Benefit Line"""

    _name = 'hr.payslip.benefit.line'
    _description = _(__doc__)

    payslip_id = fields.Many2one(
        'hr.payslip',
        'Payslip',
        required=True,
        ondelete='cascade',
    )
    category_id = fields.Many2one(
        'hr.employee.benefit.category',
        'Benefit',
        required=True,
    )
    employer_amount = fields.Float(
        'Employer Contribution',
        digits_compute=dp.get_precision('Payroll'),
    )
    employee_amount = fields.Float(
        'Employee Contribution',
        digits_compute=dp.get_precision('Payroll'),
    )
    source = fields.Selection(
        [
            ('contract', 'From Contract'),
            ('manual', 'Added Manually'),
        ],
        readonly=True,
        required=True,
        string='Type',
        type='char',
        default='manual',
    )
    reference = fields.Char('Reference')
