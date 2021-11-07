# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from fixedwidth import FixedWidth
from sicoss_registry_design import AFIP_SICOSS_v42 as AFIP_SICOSS

from odoo import models, api, fields, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def generate_file(self):
        fw_sicoss = FixedWidth(AFIP_SICOSS)
        return fw_sicoss

    def _get_payslip_work_time_data(self, payslip):
        self.ensure_one()
        normal_worked_days_obj = payslip.env["hr.payslip.worked.days"].search([('payslip_id', '=', payslip.id), ('code', '=', 'WORK100')])
        extra_worked_days_obj = payslip.env["hr.payslip.worked.days"].search([('payslip_id', '=', payslip.id), ('code', '=', 'OVT50')])
        data = {
            'normal_days': normal_worked_days_obj.number_of_days,
            'normal_hours': normal_worked_days_obj.number_of_hours,#TODO:
            'extra_hours': extra_worked_days_obj.number_of_hours
        }
        return data

    def _prepare_payslips_data(self, payslips):
        payslips_data = {}
        for payslip in payslips:
            normal_work_time_data = payslip.env["hr.payslip.worked.days"].search([('payslip_id', '=', payslip.id), ('code', '=', 'WORK100')])
            extra_work_time_data = payslip.env["hr.payslip.worked.days"].search([('payslip_id', '=', payslip.id), ('code', '=', 'WORK100')])
            current_payslip_struct = payslips_data.setdefault(
                payslip.id,
                {
                    'cuil': payslip.employee_id.cuit,  # TODO::
                    'nombre_apellido': payslip.employee_id._name,
                    'conyuge': 'N',  # TODO:
                    'cantidad_hijos': 0,
                    'codigo_situacion': payslip.contact_id.afip_situacion_revista_id.afip_id,
                    'codigo_condicion': payslip.contract_id.afip_condicion_id.afip_id,
                    'codigo_actividad': payslip.contract.afip_actividad_id.afip_id,
                    'codigo_zona': payslip.contract_id.afip_localidad_id.afip_id,
                    'poporc_adicional_ss': payslip.contract_id,  # TODO::
                    'codigo_mod_contratacion': payslip.contract_id.afip_modalidad_contratacion_id.afip_id,
                    'codigo_obra_social': payslip.contact_id.afip_obra_social_id.afip_id,
                    'cantidad_adherentes': payslip.contact_id.os_adherentes,
                    'rem_total': 0,
                    'rem_1': 0,
                    'asignaciones_familiares_pagadas': 0,
                    'importe_aporte_voluntario': payslip.contract_id.ss_aporte_adicional,
                    'importe_adicional_os': payslip.contract_id.os_aporte_adicional,
                    'importe_exedente_aportes_ss': 0,
                    'importe_exedente_aportes_os': 0,
                    'provincia_localidad': payslip,  # TODO::
                    'rem_2': 0,
                    'rem_3': 0,
                    'rem_4': 0,
                    'codigo_siniestrado': payslip.contract_id.afip_codigo_siniestrado_id.afip_id,
                    'corresponde_reduccion': 'N',  # TODO::
                    'capital_recomp_lrt': 0,
                    'tipo_empresa': payslip,  # TODO::
                    'aporte_adicional_os': 0,
                    'regimen': payslip,  # TODO:
                    'sit_revista_1': payslip,  # TODO::
                    'dia_sit_revista_1': payslip,  #TODO:
                    'sit_revista_2': payslip,  # TODO::
                    'dia_sit_revista_3': payslip,  #TODO:
                    'sit_revista_3': payslip,  # TODO::
                    'dia_sit_revista_3': payslip,  # TODO:
                    'sueldo_adiconales': 0,
                    'sac': 0,
                    'horas_extra': 0,
                    'zona_desfavorable': 0,
                    'vacaciones': 0,
                    'dias_trabajados': 30,
                    'rem_5': 0,
                    'aplica_convenio': 'S',  # TODO::
                    'rem_6': 0,
                    'tipo_operacion': payslip,  # TODO::
                    'adicionales': 0,
                    'premios': 0,
                    'rem_8': 0,
                    'rem_7': 0,
                    'cantidad_horas_extras': 0,
                    'no_remunerativo': 0,
                    'maternidad': 0,
                    'rem_9': 0,
                    'porc_tarea_diferencia': 0,
                    'horas_trabajadas': 0,
                    'svco': payslip,  # TODO:
                    'importe_detraccion': payslip.contract_id.ss_contrib_detraccion,
                    'incremento_salarial': 0,
                    'rem_11': 0,
                }
            )

            # -- Set Worked Days Details -- #
            for number_of_days, number_of_hours in normal_work_time_data and extra_work_time_data:
                current_payslip_struct['dias_trabajados'] += number_of_days
                current_payslip_struct['horas_trabajadas'] += number_of_hours
            for number_of_days, number_of_hours in extra_work_time_data:
                current_payslip_struct['cantidad_horas_extras'] += number_of_hours

            # -- Set Payslip Amounts Details -- #
            current_payslip_struct['sueldo_adicionales']
            current_payslip_struct['adicionales']
            current_payslip_struct['horas_extra']
            current_payslip_struct['sac']
            current_payslip_struct['premios']
            current_payslip_struct['zona_desfavorable']
            current_payslip_struct['no_remunerativo']
            current_payslip_struct['maternidad']

            # -- Set Remuneraciones -- #
            current_payslip_struct['rem_1']
            current_payslip_struct['rem_2']
            current_payslip_struct['rem_3']
            current_payslip_struct['rem_4']
            current_payslip_struct['rem_5']
            current_payslip_struct['rem_6']
            current_payslip_struct['rem_7']
            current_payslip_struct['rem_8']
            current_payslip_struct['rem_9']
            current_payslip_struct['rem_10']
            current_payslip_struct['rem_11']
            current_payslip_struct['rem_total']

        return payslips_data
