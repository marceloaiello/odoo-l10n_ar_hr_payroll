# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    afip_situacion_revista_id = fields.Many2one(comodel_name='hr.afip.situacion_revista', string='Situacion de Revista')
    afip_condicion_id = fields.Many2one(comodel_name='hr.afip.condicion', string='Condicion')
    afip_actividad_id = fields.Many2one(comodel_name='hr.afip.actividad', string='Actividad')
    afip_modalidad_contratacion_id = fields.Many2one(comodel_name='hr.afip.modalidad_contratacion', string='Modalidad de Contratacion')
    afip_codigo_siniestrado_id = fields.Many2one(comodel_name='hr.afip.codigo_siniestrado', string='Codigo Siniestrado')
    afip_localidad_id = fields.Many2one(comodel_name='hr.afip.localidad', string='Localidad')
    cobertura_svco = fields.Boolean(string='Con cobertura SVCO?', default="True")
    afip_obra_social_id = fields.Many2one(comodel_name='hr.afip.obra_social', string='Obra Social')
    os_adherentes = fields.Integer(string='O.S Cantidad Adherentes', default="0")
    os_aporte_adicional = fields.Float(string='O.S Aporte Adicional', default="0")
    os_contribucion_adicional = fields.Float(string='O.S Contribucion Adicional', defualt="0")
    ss_aporte_adicional = fields.Float(string='S.S Aporte Adicional', default="0")
