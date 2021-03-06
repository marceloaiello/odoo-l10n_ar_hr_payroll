# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields
from ..models.hr_fiscal_year import get_schedules


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    company_id = fields.Many2one('res.company', 'Empresa', readonly=True)
    schedule_pay = fields.Selection(get_schedules, 'Esquema de Pago', readonly=True)
