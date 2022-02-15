# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.addons.resource.models.resource import Intervals

from pytz import timezone
from datetime import datetime, time
from dateutil import rrule


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    def _weekend_intervals(self, start_dt, end_dt, resource=None):
        """ Return the weekend intervals in the given datetime range.
            The returned intervals are expressed in the resource's timezone.
        """
        tz = timezone((resource or self).tz)
        start_dt = start_dt.astimezone(tz)
        end_dt = end_dt.astimezone(tz)
        start = start_dt.date()
        until = end_dt.date()
        result = []

        weekdays = [int(attendance.dayofweek) for attendance in self.attendance_ids]
        weekends = [d for d in range(7) if d not in weekdays]
        for day in rrule.rrule(rrule.DAILY, start, until=until, byweekday=weekends):
            result.append((datetime.combine(day,time.min).astimezone(tz),
                           datetime.combine(day,time.max).astimezone(tz),self
                           ),
                          )

        return Intervals(result)

    def _attendance_intervals(self, start_dt, end_dt, resource=None):
        res = super()._attendance_intervals(start_dt=start_dt,
                                            end_dt=end_dt,
                                            resource=resource)
        if self.env.context.get('from_leave_request',False) and not self.env.context.get('exclude_weekends', False):
            weekend = self._weekend_intervals(start_dt, end_dt, resource)
            res = res | weekend
        return res
