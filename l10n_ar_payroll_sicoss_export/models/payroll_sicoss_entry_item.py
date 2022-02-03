# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from .sicoss_registry_design import AFIP_SICOSS_v42


class PayrollSicossEntryItem(models.Model):
    _name = 'payroll.sicoss_entry.item'
    _description = 'Payroll Sicoss Entry Item'

    sicoss_entry_id = fields.Many2one('payroll.sicoss_entry', string='Liquidacion AFIP-SICOSS')
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    worked_days_count = fields.Integer(string="# Dias Trabajados", default=0.00, compute='_compute_worked_days_count')
    horas_extra_count = fields.Integer(string="# Horas Extra", default=0.00, compute='_compute_horas_extra_count')
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
    importe_detraccion = fields.Float(compute='_compute_importe_detraccion', string='Importe Detraccion')
    rem_1 = fields.Float('Remuneracion 1', readonly=True, default=0.01, compute='_compute_rems')  # Base aportes SIPA
    rem_2 = fields.Float('Remuneracion 2', readonly=True, default=0.01, compute='_compute_rems')  # Base a contribuciones SIPA e INSJP
    rem_3 = fields.Float('Remuneracion 3', readonly=True, default=0.01, compute='_compute_rems')  # Base contribuciones Fondo Nacional De Empleo/Renatre y Asignaciones
    rem_4 = fields.Float('Remuneracion 4', readonly=True, default=0.01, compute='_compute_rems')  # Base aportes obra social y ANSSAL
    rem_5 = fields.Float('Remuneracion 5', readonly=True, default=0.01, compute='_compute_rems')  # Base aportes INSJP
    rem_6 = fields.Float('Remuneracion 6', readonly=True, default=0.01, compute='_compute_rems')  # No modifica
    rem_7 = fields.Float('Remuneracion 7', readonly=True, default=0.01, compute='_compute_rems')   # No modifica
    rem_8 = fields.Float('Remuneracion 8', readonly=True, default=0.01, compute='_compute_rems')  # Base contribuciones obra social y ANSSAL
    rem_9 = fields.Float('Remuneracion 9', readonly=True, default=0.01, compute='_compute_rems')   # Base LRT (ART)
    rem_10 = fields.Float('Remuneracion 10', readonly=True, default=0.01, compute='_compute_rems')  # Base contribuciones seguridad social con detraccion
    rem_11 = fields.Float('Remuneracion 11', readonly=True, default=0.01, compute='_compute_rems')  # TODO: Ver que es

    @api.depends('employee_id', 'horas_extra')
    def _compute_horas_extra_count(self):
        for record in self:
            if record.horas_extra > 0:
                record.horas_extra = 0  # TODO: Write this method
            else:
                record.horas_extra_count = 0

    @api.depends('employee_id', 'horas_extra')
    def _compute_worked_days_count(self):
        for record in self:
            record.worked_days_count = 0  # TODO: Write this method

    @api.depends()
    def _compute_importe_detraccion(self):
        pass

    @api.depends('subtotal_bruto', 'subtotal_no_remunerativo', 'importe_detraccion')
    def _compute_rems(self):
        for record in self:
            if not (record.employee_id.struct_id.name in 'NO APORT. Y CONTRIB.'):  # TODO: Deberia agregar un boolean en la structure para setear esto.
                record.rem_1 = record.subtotal_bruto
                record.rem_2 = record.subtotal_bruto
                record.rem_3 = record.subtotal_bruto
                record.rem_4 = record.subtotal_bruto
                record.rem_5 = record.subtotal_bruto
                record.rem_6 = record.rem_7 = record.subtotal_bruto
                record.rem_8 = record.subtotal_bruto
                record.rem_9 = record.subtotal_bruto + record.subtotal_no_remunerativo
                record.rem_10 = record.subtotal_bruto - record.importe_detraccion
            else:  # Caso para empleados fuera de convenio que no liquidan aportes y contribuciones (gerentes)
                record.rem_9 = record.subtotal_bruto + record.subtotal_no_remunerativo  # Solamente liquidan ART.

    @api.model
    def _compute_sicoss_entry_item(self, item):
        contract = item.employee_id.contracts[0]

        res = {
            'cuil': item.employee_id.ssnid,
            'nombre_apellido': item.employee_id.name,
            'conyuge': 'N',
            'cantidad_hijos': 0,
            'codigo_situacion': contract.afip_situacion_revista_id.afip_id,
            'codigo_condicion': contract.afip_codigo_condicion_id.afip_id,
            'codigo_actividad': contract.afip_codigo_actividad_id.afip_id,
            'codigo_zona': contract.afip_localidad_id.afip_id,
            'porc_adicional_ss': 0,
            'codigo_mod_contratacion': contract.afip_codigo_mod_contratacion_id.afip_id,
            'codigo_obra_social': contract.afip_obra_social_id.afip_id,
            'cantidad_adherentes': 0,
            'rem_total': item.subtotal_bruto + item.subtotal_no_remunerativo,
            'rem_1': item.rem_1,
            'asignaciones_familiares_pagadas': 0,
            'importe_aporte_voluntario': 0,
            'importe_adicional_os': 0,
            'importe_exedente_aportes_ss': 0,
            'importe_exedente_aportes_os': 0,
            'provincia_localidad': 0,
            'rem_2': item.rem_2,
            'rem_3': item.rem_3,
            'rem_4': item.rem_4,
            'codigo_siniestrado': contract.afip_codigo_siniestrado_id.afip_id,
            'corresponde_reduccion': 'N',
            'capital_recomp_lrt': 0,
            'tipo_empresa': 0, # TODO: Hacer esto
            'aporte_adicional_os': 0,
            'regimen': 0, # TODO: Hacer esto
            'sit_revista_1': contract.afip_situacion_revista_id.afip_id, # TODO: Ver varias situaciones de revista
            'dia_sit_revista_1': 0, # TODO: Ver varias situaciones de revista
            'sit_revista_2': contract.afip_situacion_revista_id.afip_id, # TODO: Ver varias situaciones de revista
            'dia_sit_revista_2': 0, # TODO: Ver varias situaciones de revista
            'sit_revista_3': contract.afip_situacion_revista_id.afip_id, # TODO: Ver varias situaciones de revista
            'dia_sit_revista_3': 0, # TODO: Ver varias situaciones de revista
            'sueldo_adiconales': item.sueldo,
            'sac': item.sac,
            'horas_extra': item.horas_extra,
            'zona_desfavorable': item.plus_zona_desfavorable,
            'vacaciones': item.vacaciones,
            'dias_trabajados': 30, # TODO: Ver como cambiar esto
            'rem_5': item.rem_5,
            'aplica_convenio': contract.aplica_cct,
            'rem_6': item.rem_6,
            'tipo_operacion': 0, # TODO: Ver que es esto
            'adicionales': item.adicionales,
            'premios': item.premios,
            'rem_7': item.rem_7,
            'rem_8': item.rem_8,
            'cantidad_horas_extras': 0,
            'no_remunerativo': item.no_remunerativo,
            'maternidad': item.maternidad,
            'rem_9': item.rem_9,
            'porc_tarea_diferencia': 0,
            'horas_trabajadas': 0,
            'svco': contract.cobertura_svco,
            'importe_detraccion': item.importe_detraccion,
            'incremento_salarial': item.incremento_salarial,
            'rem_11': item.rem_11,
        }


        return res
