# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
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
            result.append(
                (
                    datetime.combine(day, time.min).astimezone(tz),
                    datetime.combine(day, time.max).astimezone(tz), self
                ),
            )

        return result

    def _attendance_intervals_batch_exclude_weekends(self, start_dt, end_dt, intervals, resources, tz):
        for resource in resources:
            interval_resource = intervals[resource.id]
            attendances = []
            for attendance in interval_resource._items:
                if attendance[0].date() not in self._weekend_intervals(start_dt, end_dt, resource):
                    attendances.append(attendance)
            intervals[resource.id] = Intervals(attendances)
        return intervals

    def _attendance_intervals_batch(self, start_dt, end_dt, resources=None, domain=None, tz=None):
        res = super()._attendance_intervals_batch(start_dt=start_dt, end_dt=end_dt, resources=resources, domain=domain, tz=tz)
        if self.env.context.get("exclude_weekends") and resources:
            return self._attendance_intervals_batch_exclude_weekends(start_dt, end_dt, res, resources, tz)
        return res
