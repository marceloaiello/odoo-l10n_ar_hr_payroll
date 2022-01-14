# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class HrPeriod(models.Model):
    _inherit = 'hr.period'

    sicoss_entry_id = fields.Many2one('payroll.sicoss_entry', string='Liquidacion AFIP-SICOSS')
