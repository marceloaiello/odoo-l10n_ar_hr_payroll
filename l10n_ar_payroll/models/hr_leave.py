# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_validate(self):
        """Inject the needed context for excluding public holidays (if applicable) on the
        actions derived from this validation. This is required for example for
        `project_timesheet_holidays` for not generating the timesheet on the public holiday.
        Unfortunately, no regression test can be added, being in a separate module."""
        if self.holiday_status_id.exclude_weekends or not self.holiday_status_id:
            self = self.with_context(
                employee_id=self.employee_id.id, exclude_weekends=True
            )
        return super(HrLeave, self).action_validate()

    def _get_number_of_days(self, date_from, date_to, employee_id):
        if self.holiday_status_id.exclude_weekends or not self.holiday_status_id:
            instance = self.with_context(
                employee_id=employee_id,
                exclude_weekends=True
            )
        else:
            instance = self
        return super(HrLeave, instance)._get_number_of_days(
            date_from, date_to, employee_id
        )

    @api.depends("number_of_days")
    def _compute_number_of_hours_display(self):
        """If the leave is validated, no call to `_get_number_of_days` is done, so we
        need to inject the context here for including the public holidays if applicable.

        For such cases, we need to serialize the call to super in fragments.
        """
        to_serialize = self.filtered(
            lambda x: x.state == "validate"
            and x.holiday_status_id.exclude_weekends
        )
        for leave in to_serialize:
            leave = leave.with_context(
                exclude_weekends=True, employee_id=leave.employee_id.id
            )
            super(HrLeave, leave)._compute_number_of_hours_display()
        return super(HrLeave, self - to_serialize)._compute_number_of_hours_display()


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    exclude_weekends = fields.Boolean(string='Exclude Weekends', default=True, help=('If enabled, weekends are skipped in leave days calculation.'))
