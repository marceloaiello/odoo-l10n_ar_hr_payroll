# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_bank_titular = fields.Char(string='Titular', related="bank_account_id.acc_holder_name")
    employee_bank = fields.Char(string='Banco', related='bank_account_id.bank_id.name')
    employee_cbu = fields.Char(string='CBU', related='bank_account_id.cbu')
    employee_account_number = fields.Char(string='Numero de Cuenta', related='bank_account_id.acc_number')

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

