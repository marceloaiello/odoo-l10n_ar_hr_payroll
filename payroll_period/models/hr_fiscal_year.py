# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, models, fields, _
from odoo.exceptions import Warning as UserError

INTERVALS = {
    'annually': (relativedelta(months=12), 1),
    'semi-annually': (relativedelta(months=6), 2),
    'quaterly': (relativedelta(months=3), 4),
    'bi-monthly': (relativedelta(months=2), 6),
    'monthly': (relativedelta(months=1), 12),
    'bi-weekly': (relativedelta(weeks=2), 26),
    'weekly': (relativedelta(weeks=1), 52),
}


@api.model
def get_schedules(self):
    return [
        ('annually', _('Anual (1)')),
        ('semi-annually', _('Semestral (2)')),
        ('quarterly', _('Trimestral (4)')),
        ('bi-monthly', _('Bimensual (6)')),
        ('monthly', _('Mensual (12)')),
        ('semi-monthly', _('Quincenal (24)')),
        ('bi-weekly', _('Bisemanal (26)')),
        ('weekly', _('Semanal (52)')),
    ]


@api.model
def get_payment_days(self):
    expr = _('%s dia del siguiente periodo')
    expr_2 = _('%s dia del periodo actual')
    return [
        ('1', expr % _('Primer')),
        ('2', expr % _('Segundo')),
        ('3', expr % _('Tercer')),
        ('4', expr % _('Cuarto')),
        ('5', expr % _('Quinto')),
        ('0', expr_2 % _('Ultimo')),
    ]


class HrFiscalyear(models.Model):
    _name = 'hr.fiscalyear'
    _description = 'Hr Fiscal Year'

    @api.model
    def _default_date_start(self):
        today = datetime.now()
        return datetime(today.year, 1, 1).strftime('%Y-%m-%d')

    @api.model
    def _default_date_stop(self):
        today = datetime.now()
        return datetime(today.year, 12, 31).strftime('%Y-%m-%d')

    name = fields.Char('Año Fiscal', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_start = fields.Date(
        'Fecha Inicio',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="El primer dia del primer periodo del año fiscal.",
        default=_default_date_start
    )
    date_stop = fields.Date(
        'Fecha Fin',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="El ultimo dia del ultimo periodo del año fiscal.",
        default=_default_date_stop
    )
    period_ids = fields.One2many(
        'hr.period',
        'fiscalyear_id',
        'Periodos',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('open', 'Abierto'),
            ('done', 'Cerrado'),
        ],
        'Estado',
        readonly=True,
        default='draft'
    )
    schedule_pay = fields.Selection(
        get_schedules,
        'Pago Planificado',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default='monthly'
    )
    payment_weekday = fields.Selection(
        [
            ('0', 'Domingo'),
            ('1', 'Lunes'),
            ('2', 'Martes'),
            ('3', 'Miercoles'),
            ('4', 'Jueves'),
            ('5', 'Viernes'),
            ('6', 'Sabado'),
        ], 'Dia de Pago',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    payment_week = fields.Selection(
        [
            ('0', 'Misma Semana'),
            ('1', 'Proxima Semana'),
            ('2', 'Proxima Siguiente Semana'),
        ], 'Semana de Pago',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    payment_day = fields.Selection(
        get_payment_days,
        'Dia de Pago',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    company_id = fields.Many2one(
        'res.company',
        'Empresa',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda obj: obj.env.user.company_id
    )

    @api.onchange('schedule_pay', 'date_start')
    def onchange_schedule(self):
        if self.schedule_pay and self.date_start:
            year = self.date_start.year

            schedule_name = next((
                s[1] for s in get_schedules(self)
                if s[0] == self.schedule_pay), False)

            self.name = '%(year)s - %(schedule)s' % {
                'year': year,
                'schedule': schedule_name,
            }

    def create_periods(self):
        """
        Create every periods a payroll fiscal year
        """
        for fy in self:
            for period in fy.period_ids:
                period.unlink()

            fy.refresh()
            period_start = fy.date_start
            next_year_start = fy.date_stop + relativedelta(days=1)

            if fy.schedule_pay == 'semi-monthly':
                #  Case for semi-monthly schedules
                delta_1 = relativedelta(days=15)
                delta_2 = relativedelta(months=1)
                i = 1
                while not (period_start + delta_2 > next_year_start):
                    # create periods for one month
                    half_month = period_start + delta_1
                    fy._create_single_period(period_start, half_month, i)
                    fy._create_single_period(half_month, period_start + delta_2, i + 1)
                    # setup for next month
                    period_start += delta_2
                    i += 2
            else:  # All other cases
                delta, nb_periods = INTERVALS[fy.schedule_pay]
                i = 1
                while not (period_start + delta > next_year_start):
                    fy._create_single_period(period_start, period_start + delta, i)
                    period_start += delta
                    i += 1

    @api.model
    def _create_single_period(self, date_start, date_stop, number):
        """ Create a single payroll period
        :param date_start: the first day of the actual period
        :param date_stop: the first day of the following period
        """
        self.ensure_one()
        fy = self[0]
        date_stop -= relativedelta(days=1)
        fy.write({
            'period_ids': [(0, 0, {
                'date_start': date_start,
                'date_stop': date_stop,
                'date_payment': fy._get_day_of_payment(date_stop),
                'company_id': fy.company_id.id,
                'name': _('%s / %s-%s Periodo #%s') % (fy.name, date_start.year, date_start.month, number),
                'number': number,
                'state': 'draft',
                'schedule_pay': fy.schedule_pay,
            })],
        })

    @api.model
    def _get_day_of_payment(self, date_stop):
        """
        Get the date of payment for a period to create
        :param date_stop: the last day of the current period
        """
        self.ensure_one()
        fy = self[0]
        date_payment = date_stop
        if fy.schedule_pay in ['weekly', 'bi-weekly']:
            date_payment += relativedelta(weeks=int(fy.payment_week))
            while date_payment.strftime('%w') != fy.payment_weekday:
                date_payment -= relativedelta(days=1)
        else:
            date_payment += relativedelta(days=int(fy.payment_day))
        return date_payment

    def button_confirm(self):
        for fy in self:
            if not fy.period_ids:
                raise UserError(_('Debe crear los periodos antes de confirmar el año fiscal.'))
        self.state = 'open'
        for fy in self:
            first_period = fy.period_ids.sorted(key=lambda p: p.number)[0]
            first_period.button_open()

    def button_set_to_draft(self):
        # Set all periods to draft
        periods = self.mapped('period_ids')
        periods.button_set_to_draft()
        self.state = 'draft'

    def search_period(self, number):
        return next((p for p in self.period_ids if p.number == number),
                    self.env['hr.period'])
