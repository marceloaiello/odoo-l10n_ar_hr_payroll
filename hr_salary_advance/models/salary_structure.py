# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
class SalaryStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    max_percent = fields.Integer(string='Max.Salary Advance Percentage', help="Maximum salary advance percentage")
    advance_date = fields.Integer(string='Salary Advance-After days', help="Salary advance after days")

