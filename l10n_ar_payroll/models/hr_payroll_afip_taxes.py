# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PayrollAfipTax(models.Model):
    _name = 'payroll.afip.tax'
    _description = 'Impuestos AFIP para Sueldos'

    """ Aportes del trabajador - Alicuotas """
    aport_jubilatorio = fields.Float(string='Aportes Jubilatorios (SIPA) - Empleado', default=11.00)
    aport_insjp = fields.Float(string='Aportes I.N.S.J.P (Ley N°19.032) - Empleado', default=3.00)
    aport_os = fields.Float(string='Aportes Obra Social (OS) - Empleado', default=3.00)

    """ Contribuciones Empleador - Alicuotas """
    contrib_patronales = fields.Float(string='Contribuciones Patronales - Empleador', default=18.00)
    contrib_os = fields.Float(string='Contribuciones Obra Social (OS) - Empleador', default=6.00)
    contrib_art = fields.Float(string='Aseguradora Riesgos de Trabajo (LRT) - Empleador')
    contrib_svco = fields.Float(string='Seguro de Vida Colectivo Obligatorio (SVCO) - Empleador', default=24.35)

    """ Detracciones y Beneficios - Empleador """
    contrib_detraccion = fields.Float(string='Detraccion Contribuciones Jubilatorias (SIPA) - Empleador', default=7003.68)
    detraccion_fija_base = fields.Float(string="Detraccion de Base Imponible (con menos de 25 empleados) - Empleador", default=10000.00)
