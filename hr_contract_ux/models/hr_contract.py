# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
class HrContract(models.Model):
    _inherit = 'hr.contract'

    # We make name a computed field, but stored
    name = fields.Char(string='Referencia Contrato', compute="_compute_name", store=True)

    # Compute "Name" Based on formula so we dont need to input it manually
    @api.depends('employee_id', 'date_start')
    def _compute_name(self):
        for record in self:
            if record.employee_id:
                record.name = "Contrato de: " + record.employee_id.name + "de fecha: " + record.date_start

    # Auto calculate e"nd of trial period"
    @api.onchange('date_start')
    def _onchange_date_start(self):
        for record in self:
            if record.date_start:
                record.trial_date_end = record.date_start # SUM MONTHS TODO:


