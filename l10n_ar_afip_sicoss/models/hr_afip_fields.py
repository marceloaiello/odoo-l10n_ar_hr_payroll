from odoo import fields, models

class HrAfipSituacionRevista(models.Model):
    _name = 'hr.afip.situacion_revista'
    _description = 'AFIP: Situacion de Revista'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Referencia Situacion')

class HrAfipCondicion(models.Model):
    _name = 'hr.afip.condicion'
    _description = 'AFIP: Condicion'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Referencia Condicion')

class HrAfipActividad(models.Model):
    _name = 'hr.afip.actividad'
    _description = 'AFIP: Actividad'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Referencia Actividad')

class HrAfipModalidadContratacion(models.Model):
    _name = 'hr.afip.modalidad_contratacion'
    _description = 'AFIP: Modalidad de Contatacion'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Referencia Mod. de Contatacion')

class HrAfipCodigoSiniestrado(models.Model):
    _name = 'hr.afip.codigo_siniestrado'
    _description = 'AFIP: Codigo Siniestrado'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Referencia Cod. Siniestrado')

class HrAfipLocalidad(models.Model):
    _name = 'hr.afip.localidad'
    _description = 'AFIP: Afip Localidad'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Referencia Localidad')

class HrAfipObraSocial(models.Model):
    _name = 'hr.afip.obra_social'
    _description = 'AFIP: Afip Obra Social'

    afip_id = fields.Integer(string='Codigo AFIP')
    name = fields.Char(string='Obra Social')
