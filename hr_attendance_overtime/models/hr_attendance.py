# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    overtime_created = fields.Boolean(string=(_('¿Horas Extras?')), default=False, copy=False)
