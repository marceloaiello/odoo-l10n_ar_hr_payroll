# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

AFIP_SICOSS_v42 = {

    'cuil': {
        'required': True,
        'type': 'integer',
        'start_pos': 1,
        'end_pos': 11,
        'alignment': 'right',
        'padding': '0'
    },
    'nombre_apellido': {
        'required': True,
        'type': 'string',
        'start_pos': 12,
        'end_pos': 41,
        'alignment': 'left',
        'padding': ' '
    },
    'conyuge': {
        'required': True,
        'type': 'string',
        'start_pos': 42,
        'end_pos': 42,
        'alignment': 'left',
        'padding': ' '
    },
    'cantidad_hijos': {
        'required': True,
        'type': 'integer',
        'start_pos': 43,
        'end_pos': 44,
        'alignment': 'right',
        'padding': '0'
    },
    'codigo_situacion': {
        'required': True,
        'type': 'integer',
        'start_pos': 45,
        'end_pos': 46,
        'alignment': 'right',
        'padding': '0'
    },
    'codigo_condicion': {
        'required': True,
        'type': 'integer',
        'start_pos': 47,
        'end_pos': 48,
        'alignment': 'right',
        'padding': '0'
    },
    'codigo_actividad': {
        'required': True,
        'type': 'integer',
        'start_pos': 49,
        'end_pos': 51,
        'alignment': 'right',
        'padding': '0'
    },
    'codigo_zona': {
        'required': True,
        'type': 'integer',
        'start_pos': 52,
        'end_pos': 53,
        'alignment': 'right',
        'padding': '0'
    },
    'porc_adicional_ss': {
        'required': True,
        'type': 'integer',
        'start_pos': 54,
        'end_pos': 58,
        'alignment': 'right',
        'padding': '0'
    },
    'codigo_mod_contratacion': {
        'required': True,
        'type': 'integer',
        'start_pos': 59,
        'end_pos': 61,
        'alignment': 'right',
        'padding': '0'
    },
    'codigo_obra_social': {
        'required': True,
        'type': 'integer',
        'start_pos': 62,
        'end_pos': 67,
        'alignment': 'right',
        'padding': '0'
    },
    'cantidad_adherentes': {
        'required': True,
        'type': 'integer',
        'start_pos': 68,
        'end_pos': 69,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_total': {
        'required': True,
        'type': 'integer',
        'start_pos': 70,
        'end_pos': 81,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_1': {
        'required': True,
        'type': 'integer',
        'start_pos': 82,
        'end_pos': 93,
        'alignment': 'right',
        'padding': '0'
    },
    'asignaciones_familiares_pagadas': {
        'required': True,
        'type': 'integer',
        'start_pos': 94,
        'end_pos': 102,
        'alignment': 'right',
        'padding': '0'
    },
    'importe_aporte_voluntario': {
        'required': True,
        'type': 'integer',
        'start_pos': 103,
        'end_pos': 111,
        'alignment': 'right',
        'padding': '0'
    },
    'importe_adicional_os': {
        'required': True,
        'type': 'integer',
        'start_pos': 112,
        'end_pos': 120,
        'alignment': 'right',
        'padding': '0'
    },
    'importe_exedente_aportes_ss': {
        'required': True,
        'type': 'integer',
        'start_pos': 121,
        'end_pos': 129,
        'alignment': 'right',
        'padding': '0'
    },
    'importe_exedente_aportes_os': {
        'required': True,
        'type': 'integer',
        'start_pos': 130,
        'end_pos': 138,
        'alignment': 'right',
        'padding': '0'
    },
    'provincia_localidad': {
        'required': True,
        'type': 'string',
        'start_pos': 139,
        'end_pos': 188,
        'alignment': 'left',
        'padding': ' '
    },
    'rem_2': {
        'required': True,
        'type': 'integer',
        'start_pos': 189,
        'end_pos': 200,
        'alignment': 'right',
        'padding': ' '
    },
    'rem_3': {
        'required': True,
        'type': 'integer',
        'start_pos': 201,
        'end_pos': 212,
        'alignment': 'right',
        'padding': ' '
    },
    'rem_4': {
        'required': True,
        'type': 'integer',
        'start_pos': 213,
        'end_pos': 224,
        'alignment': 'right',
        'padding': ' '
    },
    'codigo_siniestrado': {
        'required': True,
        'type': 'integer',
        'start_pos': 225,
        'end_pos': 226,
        'alignment': 'right',
        'padding': ' '
    },
    'corresponde_reduccion': {
        'required': True,
        'type': 'string',
        'start_pos': 227,
        'end_pos': 227,
        'alignment': 'left',
        'padding': ' '
    },
    'capital_recomp_lrt': {
        'required': True,
        'type': 'integer',
        'start_pos': 228,
        'end_pos': 236,
        'alignment': 'right',
        'padding': '0'
    },
    'tipo_empresa': {
        'required': True,
        'type': 'integer',
        'start_pos': 237,
        'end_pos': 237,
        'alignment': 'right',
        'padding': '0'
    },
    'aporte_adicional_os': {
        'required': True,
        'type': 'integer',
        'start_pos': 238,
        'end_pos': 246,
        'alignment': 'right',
        'padding': '0'
    },
    'regimen': {
        'required': True,
        'type': 'integer',
        'start_pos': 247,
        'end_pos': 247,
        'alignment': 'right',
        'padding': '0'
    },
    'sit_revista_1': {
        'required': True,
        'type': 'integer',
        'start_pos': 248,
        'end_pos': 249,
        'alignment': 'right',
        'padding': '0'
    },
    'dia_sit_revista_1': {
        'required': True,
        'type': 'integer',
        'start_pos': 250,
        'end_pos': 251,
        'alignment': 'right',
        'padding': '0'
    },
    'sit_revista_2': {
        'required': True,
        'type': 'integer',
        'start_pos': 252,
        'end_pos': 253,
        'alignment': 'right',
        'padding': '0'
    },
    'dia_sit_revista_2': {
        'required': True,
        'type': 'integer',
        'start_pos': 254,
        'end_pos': 255,
        'alignment': 'right',
        'padding': '0'
    },
    'sit_revista_3': {
        'required': True,
        'type': 'integer',
        'start_pos': 256,
        'end_pos': 257,
        'alignment': 'right',
        'padding': '0'
    },
    'dia_sit_revista_3': {
        'required': True,
        'type': 'integer',
        'start_pos': 258,
        'end_pos': 259,
        'alignment': 'right',
        'padding': '0'
    },
    'sueldo_adiconales': {
        'required': True,
        'type': 'integer',
        'start_pos': 260,
        'end_pos': 271,
        'alignment': 'right',
        'padding': '0'
    },
    'sac': {
        'required': True,
        'type': 'integer',
        'start_pos': 272,
        'end_pos': 283,
        'alignment': 'right',
        'padding': '0'
    },
    'horas_extra': {
        'required': True,
        'type': 'integer',
        'start_pos': 284,
        'end_pos': 295,
        'alignment': 'right',
        'padding': '0'
    },
    'zona_desfavorable': {
        'required': True,
        'type': 'integer',
        'start_pos': 296,
        'end_pos': 307,
        'alignment': 'right',
        'padding': '0'
    },
    'vacaciones': {
        'required': True,
        'type': 'integer',
        'start_pos': 308,
        'end_pos': 319,
        'alignment': 'right',
        'padding': '0'
    },
    'dias_trabajados': {
        'required': True,
        'type': 'integer',
        'start_pos': 320,
        'end_pos': 328,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_5': {
        'required': True,
        'type': 'integer',
        'start_pos': 329,
        'end_pos': 340,
        'alignment': 'right',
        'padding': '0'
    },
    'aplica_convenio': {
        'required': True,
        'type': 'integer',
        'start_pos': 341,
        'end_pos': 341,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_6': {
        'required': True,
        'type': 'integer',
        'start_pos': 342,
        'end_pos': 353,
        'alignment': 'right',
        'padding': '0'
    },
    'tipo_operacion': {
        'required': True,
        'type': 'integer',
        'start_pos': 354,
        'end_pos': 354,
        'alignment': 'right',
        'padding': '0'
    },
    'adicionales': {
        'required': True,
        'type': 'integer',
        'start_pos': 355,
        'end_pos': 366,
        'alignment': 'right',
        'padding': '0'
    },
    'premios': {
        'required': True,
        'type': 'integer',
        'start_pos': 367,
        'end_pos': 378,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_8': {
        'required': True,
        'type': 'integer',
        'start_pos': 379,
        'end_pos': 390,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_7': {
        'required': True,
        'type': 'integer',
        'start_pos': 391,
        'end_pos': 402,
        'alignment': 'right',
        'padding': '0'
    },
    'cantidad_horas_extras': {
        'required': True,
        'type': 'integer',
        'start_pos': 403,
        'end_pos': 405,
        'alignment': 'right',
        'padding': '0'
    },
    'no_remunerativo': {
        'required': True,
        'type': 'integer',
        'start_pos': 406,
        'end_pos': 417,
        'alignment': 'right',
        'padding': '0'
    },
    'maternidad': {
        'required': True,
        'type': 'integer',
        'start_pos': 418,
        'end_pos': 429,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_9': {
        'required': True,
        'type': 'integer',
        'start_pos': 439,
        'end_pos': 450,
        'alignment': 'right',
        'padding': '0'
    },
    'porc_tarea_diferencia': {
        'required': True,
        'type': 'integer',
        'start_pos': 451,
        'end_pos': 459,
        'alignment': 'right',
        'padding': '0'
    },
    'horas_trabajadas': {
        'required': True,
        'type': 'integer',
        'start_pos': 460,
        'end_pos': 462,
        'alignment': 'right',
        'padding': '0'
    },
    'svco': {
        'required': True,
        'type': 'integer',
        'start_pos': 463,
        'end_pos': 463,
        'alignment': 'right',
        'padding': '0'
    },
    'importe_detraccion': {
        'required': True,
        'type': 'integer',
        'start_pos': 464,
        'end_pos': 475,
        'alignment': 'right',
        'padding': '0'
    },
    'incremento_salarial': {
        'required': True,
        'type': 'integer',
        'start_pos': 476,
        'end_pos': 487,
        'alignment': 'right',
        'padding': '0'
    },
    'rem_11': {
        'required': True,
        'type': 'integer',
        'start_pos': 488,
        'end_pos': 499,
        'alignment': 'right',
        'padding': '0'
    },
}
