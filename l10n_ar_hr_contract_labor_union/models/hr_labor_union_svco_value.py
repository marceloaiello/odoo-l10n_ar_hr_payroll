# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrLaborUnionSvcoValue(models.Model):
    _name = 'hr.labor_union.svco_value'
    _description = 'Valores de S.V.C.O de C.C.T'

    name = fields.Char(string='Valor S.V.C.O')
    from_date = fields.Date(string='Vigencia Desde', required=True, help='Fecha de Fin, incluida en el rango.')
    to_date = fields.Date(string='Vigencia Hasta', required=True, help='Fecha de Inicio, incluida en el rango.')
    value = fields.Float(string='Valor / Precio', required=True)
    labor_union_id = fields.Many2one(comodel_name='hr.labor_union', string='C.C.T / Sindicato', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    @api.constrains('to_date', 'from_date', 'company_id')
    def _check_svco_dates(self):
        for record in self:
            if record.from_date == record.to_date:
                raise ValidationError("'Fecha Desde' y 'Fecha Hasta' no pueden ser el mismo valor.")
            if record.to_date < record.from_date:
                raise ValidationError("'Fecha Hasta' no puede ser menor a 'Fecha Desde'.")
            domain = [
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id),
                    '|', '|',
                    '&', ('from_date', '<=', record.from_date), ('to_date', '>=', record.from_date),
                    '&', ('from_date', '<=', record.to_date), ('to_date', '>=', record.to_date),
                    '&', ('from_date', '<=', record.from_date), ('to_date', '>=', record.to_date),
                ]
            if self.search_count(domain) > 0:
                raise ValidationError(_('No puedes ingresra fechas que se superpongan a los periodos ya ingresados de S.V.C.O.'))
        return True
