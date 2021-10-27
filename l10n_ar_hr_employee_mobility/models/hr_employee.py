# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    shell_flota_cod_conductor = fields.Char(
        string="Shell Flota - Codigo Conductor",
        groups="hr.group_hr_manager"
    )
