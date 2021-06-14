from odoo import api, fields, models

class ContractAfip(models.Model):
    _inherit = 'hr.contract'

    afip_situacion_revista_id = fields.Many2one(comodel_name='hr.afip.situacion_revista', string='Situacion de Revista',
        default="Activo")
    afip_condicion_id = fields.Many2one(comodel_name='hr.afip.condicion', string='Condicion',
        default="A Tiempo completo indeterminado / Trabajo permanente")
    afip_actividad_id = fields.Many2one(comodel_name='hr.afip.actividad', string='Actividad',
        default="Actividades no clasificadas")
    afip_modalidad_contratacion_id = fields.Many2one(comodel_name='hr.afip.modalidad_contratacion', string='Modalidad de Contratacion',
        default="SERVICIOS COMUNES Mayor de 18 años")
    afip_codigo_siniestrado_id = fields.Many2one(comodel_name='hr.afip.codigo_siniestrado', string='Codigo Siniestrado',
        default="No Incapacitado")
    afip_localidad_id = fields.Many2one(comodel_name='hr.afip.localidad', string='Localidad',
        default="CAPITAL FEDERAL")
    cobertura_svco = fields.Boolean(string='Con cobertura SVCO?', default="True")
    obra_social_id = fields.Many2one(comodel_name='hr.afip.obra_social', string='Obra Social')
    os_adherentes = fields.Integer(string='Cantidad Adherentes', default="0")
    os_aporte_adicional = fields.Float(string='Aporte Adicional', default="0")
    os_contribucion_adicional = fields.Float(string='Contribucion Adicional', defualt="0")
    ss_aporte_adicional = fields.Float(string='Aporte Adicional', default="0")



