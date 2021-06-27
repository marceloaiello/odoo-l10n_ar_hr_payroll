# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exceptions, _


class HrLaborUnionCategory(models.Model):
    _name = 'hr.labor_union.category'
    _description = 'Categorias de C.C.T / Sindicatos'
    _check_company_auto = True

    name = fields.Char(string='Categoria C.C.T', required=True)
    category_period_type = fields.Selection(string="Periodo de Importe",
                                            selection=[
                                                ("hour", "Por Hora"),
                                                ("day", "Diario"),
                                                ("week", "Semanal"),
                                                ("month", "Mensual"),
                                                ("quarter", "Quincenal"),
                                                ("year", "Anual"),
                                            ],
                                            default="hour",
                                            help="Periodo de calculo del importe registrado",
                                            )
    current_value = fields.Monetary(
        compute="_compute_current_value", string='Valor Actual')
    categories_prices = fields.One2many(comodel_name='hr.labor_union.category.price', inverse_name='labor_union_category_id',
                                        string='Valores de Categoria')
    labor_union_id = fields.Many2one(comodel_name='hr.labor_union', string='C.C.T / Sindicato',
                                     required=True, ondelete="cascade", check_company=True, options="{'currency_field': 'currency_id'}")
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Empresa', required=True,
                                 default=lambda self: self.env.user.company_id)

    @api.depends('categories_prices')
    def _compute_current_value(self):
        for record in self:
            today = fields.Date.context_today(self).strftime('%Y-%m-%d')
            category_value = 0
            domain = [('labor_union_category_id', '=', record.id),
                      ('from_date', '<=', today), ('to_date', '>=', today)]
            if record.categories_prices.search_count(domain) == 1:
                for cprice in record.categories_prices.search(domain):
                    category_value = cprice.value
            record.current_value = category_value


class HrLaborUnionCategoryPrice(models.Model):
    _name = 'hr.labor_union.category.price'
    _description = 'Valores de Categorias C.C.T'
    _check_company_auto = True

    name = fields.Char(string='Referencia', readonly=True)
    from_date = fields.Date(string='Fecha Desde', required=True)
    to_date = fields.Date(string='Fecha Hasta', required=True)
    value = fields.Monetary(string='Valor Actual', required=True,
                            options="{'currency_field': 'currency_id'}")
    labor_union_category_id = fields.Many2one(comodel_name='hr.labor_union.category', string='C.C.T Categorias - Precios',
                                              equired=True, ondelete="cascade", check_company=True)
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Empresa', required=True,
                                 default=lambda self: self.env.user.company_id)

    @api.onchange("labor_union_category_id", "from_date", "to_date")
    def _onchange_labor_union_category_dates(self):
        if self.labor_union_category_id or self.from_date or self.to_date:
            self.name = "Categoria: " + self.labor_union_category_id.name + \
                " >> " + "Desde " + self.from_date + "Hasta " + self.to_date

    @api.constrains('to_date', 'from_date', 'company_id', 'labor_union_category_id')
    def _check_category_dates(self):
        """ make sure dates dont overlap """
        for record in self:
            if record.from_date == record.to_date:
                raise exceptions.ValidationError(
                    _("'Fecha Desde' y 'Fecha Hasta' no pueden ser el mismo valor."))
            if record.to_date < record.from_date:
                raise exceptions.ValidationError(
                    _("'Fecha Hasta' no puede ser menor a 'Fecha Desde'."))
            domain = [
                ('id', '!=', record.id),
                ('labor_union_category_id', '=', record.labor_union_category_id.id),
                ('company_id', '=', record.company_id.id),
                '|', '|',
                '&', ('from_date', '<=', record.from_date), ('to_date',
                                                             '>=', record.from_date),
                '&', ('from_date', '<=', record.to_date), ('to_date',
                                                           '>=', record.to_date),
                '&', ('from_date', '<=', record.from_date), ('to_date',
                                                             '>=', record.to_date),
            ]
            if self.search_count(domain) > 0:
                raise exceptions.ValidationError(
                    _('No puedes ingresar fechas que se superpongan a los periodos ya ingresados de categorias.'))
