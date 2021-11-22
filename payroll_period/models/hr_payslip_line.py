# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    hr_period_id = fields.Many2one(
        'hr.period',
        related='slip_id.hr_period_id',
        string='Periodo',
        store=True,
        readonly=True,
    )
