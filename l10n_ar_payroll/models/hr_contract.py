# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    afip_situacion_revista_id = fields.Many2one(
        comodel_name='hr.afip.situacion_revista', string='Situacion de Revista')  # TODO: Debe ser dinamico
    afip_condicion_id = fields.Many2one(
        comodel_name='hr.afip.condicion', string='Condicion')
    afip_actividad_id = fields.Many2one(
        comodel_name='hr.afip.actividad', string='Actividad')
    afip_modalidad_contratacion_id = fields.Many2one(
        comodel_name='hr.afip.modalidad_contratacion', string='Modalidad de Contratacion')
    afip_codigo_siniestrado_id = fields.Many2one(
        comodel_name='hr.afip.codigo_siniestrado', string='Codigo Siniestrado')  # TODO: Debe ser dinamico
    afip_localidad_id = fields.Many2one(
        comodel_name='hr.afip.localidad', string='Localidad')
    cobertura_svco = fields.Boolean(string='Con cobertura SVCO?', default="True")
    afip_obra_social_id = fields.Many2one(
        comodel_name='hr.afip.obra_social', string='Obra Social')
    os_adherentes = fields.Integer(string='Cantidad Adherentes', default="0")
    os_aporte_adicional = fields.Float(string='Aporte Adicional', default="0")
    os_contribucion_adicional = fields.Float(
        string='Contribucion Adicional', default="0")
    ss_aporte_adicional = fields.Float(string='Aporte Adicional', default="0")
    ss_contrib_detraccion = fields.Float(
        string="SS - Detraccion Contribuciones", default='7003.8')
    # Link with contract advantges templates
    hr_contract_advantage_ids = fields.One2many(
        'hr.contract.advantage', 'contract_id', string='Parametros Adicionales')

    # TODO: Action para computar ILT temporaria, se debe cambiar el campo de Situacion de Revista y el de Codigo de siniestrado.

    # TODO: Action para computar la baja del empleado, se debe hacer un wizard donde se indique, motivo de baja, fe cha de telegrama (si correspondiera) y se
    # cambia estado "Situacion de Revista" al correspondiente.

    # TODO: Se debe realizar un schedule job para cambiar la condicion de contratacion la cual debe ser en principio periodo de prueba (y no editable) y luego de
    # pasado el plazo de prueba cambiar a Servicios Comunes (y se habilita para poder modificar manualmente). Managers deben tener posibilidad de desbloquear todo.

    # TODO: Modalidad de contratacion creo que debe ser manual segun el estado de la persona. No vale la pena meter dinamismo ahi. Misma logica para los campos "Actividad",
    # "Localidad" y "Obra Social"

    # TODO: La detraccion debe calcularse segun la actividad informada y el tipo de liquidacion (siempre calcularse la maxima, y agregar un checkbox para editarla manualmente).

    # TODO: Tema aportes adicionales no es muy comun que se realice, al menos no en mi caso, pero estan los campos completamente editables en el contrato. De todas formas, quiza
    # puerda darle un poco de dinamismo en el futuro. El

    # TODO: Ver como funciona el tema de los Adherentes y entonces ver que hacer con ese campo.



