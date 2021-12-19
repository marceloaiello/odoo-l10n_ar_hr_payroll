# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class HrSussItem(models.Model):
    _name = 'hr.suss.item'
    _description = 'Hr Suss Item'

    name = fields.Char(string='Referencia')
    period_id = fields.Many2one('hr.period', string='Periodo Fiscal')
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    sueldo = fields.Float(string='Sueldo')
    adicionales = fields.Float(string='Adicionales')
    horas_extra = fields.Float(string='Horas Extra')
    vacaciones = fields.Float(string='Vacaciones')
    plus_zona_desfavorable = fields.Float(string='Plus Zona Desfavorable')
    sac = fields.Float(string='S.A.C')
    premios = fields.Float(string='Premios')
    no_remunerativo = fields.Float(string='No Remunerativo')
    maternidad = fields.Float(string='Maternidad')
    incremento_salarial = fields.Float(string='Incremento Salarial')
    rectificativa_remuneracion = fields.Float(string='Rectificativa Remuneracion')
    subtotal_bruto = fields.Float(string='Subtotal Bruto')
    subtotal_no_remunerativo = fields.Float(string='Subtotal No Remunerativo')
    subtotal_descuentos = fields.Float(string='Subtotal Descuentos')
    subtotal_neto = fields.Float(string='Subtotal Neto')
