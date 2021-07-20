# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from pytz import utc

from odoo import models, api, fields


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    attendance_overtime = fields.Float(
        compute='_compute_worked_hours', string='Horas Extra', store=True, readonly=True)

    # We inherit the worked hours computation to distinguish between overtime and normal hours.
    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                attendance.worked_hours = delta.total_seconds() / 3600.0
                if attendance.employee_id.contract_id.allow_extra_hours:
                    if attendance.worked_hours > attendance.theorical_hours:
                        attendance.attendance_overtime = attendance.worked_hours - attendance.theorical_hours
                    else:
                        attendance.attendance_overtime = False
                else:
                    attendance.attendance_overtime = False
            else:
                attendance.worked_hours = False
                attendance.attendance_overtime = False

    # This allow us to get the values of hr_attendance records and return a dict containing total types of hours.
    # It is used in payslips to calculate aditional concepts.
    # TODO: We have to extend that class to use hr_attendance in payslips, because payslip uses work_time by default and its okay.
    def _get_attendance_hours_in_timeframe(self, from_date, to_date):
        for employee in self:
            start = from_date.astimezone(utc).replace(
                tzinfo=None)  # TODO: Ver el tema de timezone
            end = to_date.astimezone(utc).replace(tzinfo=None)
            attendance_data = {}
            result = {}

            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                '&',
                ('check_in', '<=', end),
                ('check_out', '>=', start),
            ])

            for attendance in attendances:
                attendance_data['overtime_hours'] += attendance.overtime_hours
                attendance_data['normal_hours'] += attendance.theorical_hours
                attendance_data['total_hours'] += attendance.worked_hours

            result[employee.id] = attendance_data

        return result
