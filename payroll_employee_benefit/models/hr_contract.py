# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    benefit_line_ids = fields.One2many(
        'hr.employee.benefit',
        'contract_id',
        'Employee Benefits',
    )
