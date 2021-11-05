# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api, fields


class HrHolidaysPublic(models.Model):
    _inherit = 'hr.holidays.public.line'

    leave_id = fields.Many2one("hr.leave", string="Leave")

    def _public_holidays_leaves_struct(self):
        for record in self:
            hr_leave_struct = {
                'holidays_status_id': self.env.ref('hr_holidays_public_leave.leaves_HFRD'),
                'request_date_from': record.date,
                'request_date_to': record.date,
                'name': record.name,
                'holiday_type': 'company',
                'mode_company_id': self.env.company.id,
                'payslip_status': False,
                'state': 'validate'
            }

        return hr_leave_struct

    @api.constrains("date", "name", "year_id", "state_ids")
    def _update_calendar_event(self):
        for rec in self:
            if rec.meeting_id:
                rec.meeting_id.write(rec._prepare_holidays_meeting_values())
            if rec.leave_id:
                rec.leave_id.write(rec.__public_holidays_leaves_struct())

    @api.model
    def create(self, values):
        res = super().create(values)
        res.meeting_id = self.env["calendar.event"].create(
            res._prepare_holidays_meeting_values()
        )
        res.leave_id = self.env["hr.leave"].create(
            res.__public_holidays_leaves_struct()
        )
        return res
