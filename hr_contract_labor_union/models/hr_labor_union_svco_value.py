# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exceptions, _


class HrLaborUnionSvcoValue(models.Model):
    _name = 'hr.labor_union.svco_value'
    _description = 'Valores de S.V.C.O de C.C.T'
    _check_company_auto = True

    name = fields.Char(string='Referencia', readonly=True)
    from_date = fields.Date(string='Fecha Desde', required=True,
                            help='Fecha de Fin, incluida en el rango.')
    to_date = fields.Date(string='Fecha Hasta', required=True,
                          help='Fecha de Inicio, incluida en el rango.')
    value = fields.Monetary(string='Valor', required=True,
                            options="{'currency_field': 'currency_id'}")
    labor_union_id = fields.Many2one(
        comodel_name='hr.labor_union', string='C.C.T / Sindicato', required=True, ondelete="cascade", check_company=True)
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Empresa', required=True,
                                 default=lambda self: self.env.user.company_id)

    @api.onchange("labor_union_id", "from_date", "to_date")
    def _onchange_labor_union_dates(self):
        if self.labor_union_id and self.from_date and self.to_date:
            self.name = "SVCO: " + self.labor_union_id.name + " >> " + \
                "Desde " + self.from_date.strftime("%d/%m/%Y") + " Hasta " + self.to_date.strftime("%d/%m/%Y")

    @api.constrains('to_date', 'from_date', 'company_id', 'labor_union_id')
    def _check_svco_dates(self):
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
                ('labor_union_id', '=', record.labor_union_id.id),
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
                    _('No puedes ingresra fechas que se superpongan a los periodos ya ingresados de S.V.C.O.'))
            return True
