# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

# TODO: Debemos buscar la forma de setear estos campos por default, dado que en la mayoria de los casos no cambian.
# TODO: Mostrar el "name" con el codigo de afip (para poder buscar con codigo) => ( COD AFIP ) NAME


class HrAfipSituacionRevista(models.Model):
    """
    AFIP: Situacion de Revista

    Estos modelos se crean para poder seleccionar en contratos
    los diferentes campos y caracterizaciones que se necesitan informar
    en AFIP.
    """
    _name = 'hr.afip.situacion_revista'
    _description = 'AFIP: Situacion de Revista'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Ref. Situacion')


class HrAfipCondicion(models.Model):
    """
    AFIP: Condicion de Contratacion

    Estos modelos se crean para poder seleccionar en contratos
    los diferentes campos y caracterizaciones que se necesitan informar
    en AFIP.
    """
    _name = 'hr.afip.condicion'
    _description = 'AFIP: Condicion'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Ref. Condicion')


class HrAfipActividad(models.Model):
    """
    AFIP: Condicion tipo de Actividad

    Estos modelos se crean para poder seleccionar en contratos
    los diferentes campos y caracterizaciones que se necesitan informar
    en AFIP.
    """
    _name = 'hr.afip.actividad'
    _description = 'AFIP: Actividad'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Ref. Actividad')


class HrAfipModalidadContratacion(models.Model):
    """
    AFIP: Modalidad de Contratacion

    Estos modelos se crean para poder seleccionar en contratos
    los diferentes campos y caracterizaciones que se necesitan informar
    en AFIP.
    """
    # TODO: Este campo deberia ser dinamico para mostrar por default "Periodo de Prueba" en los primeros 3 meses del contrato y luego pasar a "Activo"
    # TODO: Hint: Se debe usar la fecha del contrato con alguna accion planificada (cron). Pero debe ser editable para cubrir los casos donde no se use asi.
    # TODO: Hint: Boolean de editable? Setting?
    _name = 'hr.afip.modalidad_contratacion'
    _description = 'AFIP: Modalidad de Contatacion'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Ref. Mod. de Contatacion')


class HrAfipCodigoSiniestrado(models.Model):
    """
    AFIP: Codigo Siniestrado

    Estos modelos se crean para poder seleccionar en contratos
    los diferentes campos y caracterizaciones que se necesitan informar
    en AFIP.
    """
    # TODO: (Solo debe aparecer cuando el estado de revista es ILT o ILTT, sino se informara "No Siniestrado"
    # TODO: Hint: Como vamos a registar los siniestros?
    _name = 'hr.afip.codigo_siniestrado'
    _description = 'AFIP: Codigo Siniestrado'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Ref. Cod. Siniestrado')


class HrAfipLocalidad(models.Model):
    """
    AFIP: Codigo de Localidades

    Estos modelos se crean para poder seleccionar en contratos
    los diferentes campos y caracterizaciones que se necesitan informar
    en AFIP.
    """
    _name = 'hr.afip.localidad'
    _description = 'AFIP: Afip Localidad'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Ref. Localidad')


class HrAfipObraSocial(models.Model):
    """
    AFIP: Obra Social del Trabajador

    Estos modelos se crean para poder seleccionar en contratos
    los diferentes campos y caracterizaciones que se necesitan informar
    en AFIP.
    """
    _name = 'hr.afip.obra_social'
    _description = 'AFIP: Afip Obra Social'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Obra Social')
