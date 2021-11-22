# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.addons import decimal_precision as dp
from .hr_employee_benefit_rate import get_amount_types


class HrEmployeeBenefitRateLine(models.Model):
    _name = 'hr.employee.benefit.rate.line'
    _description = 'Hr Employee Benefit Rate Line'
    _order = 'date_start desc'

    employee_amount = fields.Float(
        'Employee Amount',
        required=True,
        digits_compute=dp.get_precision('Payroll'),
    )
    employer_amount = fields.Float(
        'Employer Amount',
        required=True,
        digits_compute=dp.get_precision('Payroll'),
    )
    date_start = fields.Date(
        'Start Date',
        required=True,
        default=fields.Date.context_today,
    )
    date_end = fields.Date('End Date')
    parent_id = fields.Many2one(
        'hr.employee.benefit.rate',
        'Parent',
        ondelete='cascade',
        required=True,
    )
    amount_type = fields.Selection(
        get_amount_types,
        related='parent_id.amount_type',
        string="Amount Type",
        readonly=True,
    )
    category_id = fields.Many2one(
        'hr.employee.benefit.category',
        related='parent_id.category_id',
        string="Category",
        readonly=True,
    )
