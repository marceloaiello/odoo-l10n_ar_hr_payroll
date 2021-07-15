# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    # Auto calculate end of trial period, acording to default Argentina LCT 3 Months of trial period
    @api.onchange('date_start')
    def _onchange_date_start(self):
        for record in self:
            if record.date_start:
                record.trial_date_end = record.date_start
