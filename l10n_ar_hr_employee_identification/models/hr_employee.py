# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    identification_type_id = fields.Many2one(
        string="hr.employee.identification.type",
        groups="hr.group_hr_user"
    )
    identification_expiry_date = fields.Date(
        string="Identification expiry",
        groups="hr.group_hr_user"
    )
    identification_tram_number = fields.Char(
        string="Numero de Tramite (ARG)",
        groups="hr.group_hr_user"
    )
    identification_scan_image = fields.Binary(
        string='ID Attachment',
        groups="hr.group_hr_user"
    )
