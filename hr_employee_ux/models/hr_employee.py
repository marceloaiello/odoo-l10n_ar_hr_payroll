# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Extract the document number from cuil
    @api.onchange('identification_id')
    def _compute_passport_id(self):
        for record in self:
            if record.identification_id:
                record.passport_id = record.identification_id.split('-')[1]

    # Badge code and password is DNI
    @api.onchange('passport_id')
    def _compute_attendance_badge_codes(self):
        for record in self:
            if record.passport_id:
                record.pin = record.passport_id
                record.barcode = record.passport_id

