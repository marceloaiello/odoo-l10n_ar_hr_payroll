# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployeeBenefitCategory(models.Model):
    _name = 'hr.employee.benefit.category'
    _description = 'Employee Benefit Categories'

    name = fields.Char('Benefit Name', required=True)
    code = fields.Char(
        'Code',
        help="The code that can be used in the salary rules to identify "
        "the benefit",
    )
    description = fields.Text(
        'Description',
        help="Brief explanation of which benefits the category contains."
    )
    salary_rule_ids = fields.Many2many(
        'hr.salary.rule', 'salary_rule_employee_benefit_rel',
        'benefit_id', 'salary_rule_id', 'Salary Rules',
    )
    rate_ids = fields.One2many(
        'hr.employee.benefit.rate',
        'category_id',
        string="Benefit Rates",
    )
    reference = fields.Char(
        'Reference',
        help="Field used to enter an external identifier for a "
        "benefit category. Example, pension plans may have a "
        "registration number."
    )
    active = fields.Boolean('active', default=True)
