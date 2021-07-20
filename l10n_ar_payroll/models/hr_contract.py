# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class HrContract(models.Model):
    _inherit = 'hr.contract'

    allow_extra_hours = fields.Boolean(string='Permitir computo de horas extra')
