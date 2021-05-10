# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HrLaborUnion(models.Model):
    _name = 'hr.labor_union'
    _description = 'Union Laboral / Sindicatos'

    name = fields.Char(string='Name')
    sindicato = fields.String(string='Sindicato')
    convenio = fields.String(string='Codigo C.C.T / RAMA')
    cct_categories = fields.One2many(comodel_name='hr.labor_union.category',inverse_name='labor_union_id',
                                        string='Categorias C.C.T')
    cct_svco_values = fields.One2many(comodel_name='hr.labor_union.svco_value',inverse_name='labor_union_id',
                                        string='S.V.C.O / Seguro de Vida')
    current_value = fields.Float(compute='_compute_current_value', string='Valor Actual - SVCO')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    @api.depends('cct_svco_values')
    def _compute_current_value(self):
        for record in self.cct_svco_values:
            svco_value = 0
            if record.from_date <= today() <= record.to_date:
                svco_value = record.value
        record.svco_current_value = svco_value


class HrLaborUnionCategory(models.Model):
    _name = 'hr.labor_union.category'
    _description = 'Categorias de C.C.T'

    name = fields.Char(string='Categoria C.C.T', required=True)
    current_value = fields.Float(string='Valor / Precio', computed="_compute_current_value")
    categories_prices = fields.One2many(comodel_name='hr.labor_union.category.price', inverse_name='labor_union_category_id', string='Valores de Categoria')
    labor_union_id = fields.Many2one(comodel_name='hr.labor_union', string='C.C.T / Sindicato', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    @api.depends('categories_prices')
    def _compute_current_value(self):
        for record in self.categories_prices:
            value = 0
            if record.date_from <= today() <= record.date_to:
                value = record.value
        record.current_value = value

class HrLaborUnionCategoryValue(models.Model):
    _name = 'hr.labor_union.category.price'
    _description = 'Precios de Categorias C.C.T'

    name = fields.Char(string='Categoria C.C.T', required=True)
    date_from = fields.Date(string='Fecha Desde', required=True)
    date_to = fields.Date(string='Fecha Hasta', required=True)
    value = fields.Float(string='Valor / Precio', required=True)
    labor_union_category_id = fields.Many2one(comodel_name='hr.labor_union.category', string='C.C.T Category Price', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    @api.constrains('to_date', 'from_date', 'company_id')
    def _check_dates(self):
        for record in self:
            if record.date_from == record.date_to
                raise ValidationError("'Fecha Desde' y 'Fecha Hasta' no pueden ser el mismo valor.")
            if record.date_to < record.date_from:
                raise ValidationError("'Fecha Hasta' no puede ser menor a 'Fecha Desde'.")
            domain = [
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id),
                    '|', '|',
                    '&', ('from_date', '<=', record.date_from), ('to_date', '>=', record.date_from),
                    '&', ('from_date', '<=', record.date_to), ('to_date', '>=', record.date_to),
                    '&', ('from_date', '<=', record.date_from), ('to_date', '>=', record.date_to),
                ]
            if self.search_count(domain) > 0:
                raise ValidationError(_('No puedes ingresar fechas que se superpongan a los periodos ya ingresados de categorias.'))
        return True

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
            if record.from_date == record.to_date
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





