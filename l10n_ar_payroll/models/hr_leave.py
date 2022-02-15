# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.onchange('holiday_status_id')
    def recompute_no_days(self):
        self._onchange_leave_dates()

    def _get_number_of_days(self, date_from, date_to, employee_id):
        context_data = {'employee_id': employee_id,
                        'from_leave_request': True,
                        'exclude_weekends': False}

        if (self.holiday_status_id.exclude_weekends or
                not self.holiday_status_id):
            context_data['exclude_weekends'] = True

        instance = self.with_context(context_data)
        return super(HrLeave, instance)._get_number_of_days(
            date_from,
            date_to,
            employee_id,
        )


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    exclude_weekends = fields.Boolean(
        string='Exclude Weekends',
        default=True,
        help=(
            'If enabled, weekends are skipped in leave days'
            ' calculation.'
        ),
    )
