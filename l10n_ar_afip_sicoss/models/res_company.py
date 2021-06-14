from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    afip_sicoss_type = fields.Selection([
        ('0', 'Administracion Publica',
         '1', 'Dto. 814/01, art. 2, inc. b).',
         '2', 'Servicios eventuales. Dto. 814/01, art. 2, inc. b).',
         '3', 'Provincias u otros.',
         '4', 'Dto. 814/01, art. 2, inc. a).',
         '5', 'Servicios eventuales. Dto. 814/01, art. 2, inc. a).',
         '6', 'Dto. 814/01, art. 2, inc. b). Provincias. Ley 22.016.',
         '7', 'Colegios privados.')
    ], string='AFIP SICOSS - Tipo Empleador', default="TODO", help="Para seleccionar este campo correctamente, verificar en sus Form931 Anteriores.")
