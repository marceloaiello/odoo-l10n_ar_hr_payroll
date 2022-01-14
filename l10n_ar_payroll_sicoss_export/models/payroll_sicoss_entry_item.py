# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PayrollSicossEntryItem(models.Model):
    _name = 'payroll.sicoss_entry.item'
    _description = 'Payroll Sicoss Entry Item'

    sicoss_entry_id = fields.Many2one('payroll.sicoss_entry', string='Liquidacion AFIP-SICOSS')
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
