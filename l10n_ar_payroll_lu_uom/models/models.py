# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import UserError
from datetime import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def _get_month_gross(self, payslip):
        amount_sum = 0.00

        affected_payslips = self.env['hr.payslip'].search([
            ('employee_id', '=', payslip.employee_id),
            ('date_from', '>=', payslip.date_from.replace(day=1)),
            ('date_to', '<=', payslip.date_from)])

        if len(affected_payslips):
            for ap in affected_payslips:
                for line in ap.details_by_salary_rule_category.filtered(lambda r: r.category_id.code in ['TGROSS', 'TNOREM', 'VAC931', 'EXT931']):
                    if line.category_id.code == 'TGROSS':
                        amount_sum += line.total
                    if line.category_id.code == 'TNOREM':
                        amount_sum += line.total
                    if line.category_id.code == 'EXT931':
                        amount_sum -= line.total
                    if line.category_id.code == 'VAC931':
                        amount_sum -= line.total

        return amount_sum

    @api.model
    def compute_imgr(self, contract=False, categories=False, payslip=False):
        # Si el empleado es de liquidacion mensual, se utilizan solo los valores de la liquidacion actual
        # para calcular el IMGR. Si es de caracter quincenal, se buscan los valores de liquidacioens anteriores y
        # se suman a la actual.
        # TODO: Contemplar otros tipos de declaraciones en el flujo.
        imgr_value = 61688.00
        category_sum = 0.00
        if contract.schedule_pay == 'monthly':
            category_sum = categories.GROSS + categories.NOREM
            if categories.EXT931 and categories.EXT931 > 0:
                category_sum -= categories.EXT931
            if categories.VAC931 and categories.VAC931 > 0:
                category_sum -= categories.VAC931
        elif contract.schedule_pay == 'bi-weekly':
            category_sum = self._get_month_gross(payslip) + categories.GROSS + categories.NOREM
            if categories.EXT931 and categories.EXT931 > 0:
                category_sum -= categories.EXT931
            if categories.VAC931 and categories.VAC931 > 0:
                category_sum -= categories.VAC931
        else:
            raise UserError('ERROR: La frecuencia de pago del empleado no es valida para el calculo del IMGR.')

        # Get full and real worked days in the month and proporcionate the IMGR Base Amount
        full_work_days = contract.employee_id._get_work_days_data(
            datetime.combine(payslip.date_from.replace(day=1), datetime.min.time()),
            datetime.combine(payslip.date_to, datetime.max.time()),
            calendar=contract.resource_calendar_id,
            compute_leaves=False)["days"]
        real_worked_days = contract.employee_id._get_work_days_data(
            datetime.combine(payslip.date_from.replace(day=1), datetime.min.time()),
            datetime.combine(payslip.date_to, datetime.max.time()),
            calendar=contract.resource_calendar_id,
            compute_leaves=True)["days"]
        if full_work_days > real_worked_days:
            imgr_base = real_worked_days * (imgr_value / full_work_days)
        else:
            imgr_base = imgr_value

        # Comparamos el imgr con el bruto imponible, para ver si es necesario proporcionar el monto.
        if category_sum < imgr_base:
            amount = imgr_base - category_sum
        elif category_sum >= imgr_base:
            amount = 0.00

        return amount


class HrContractLaborUnionCategoryPrice(models.Model):
    _inherit = 'hr.labor_union.category.price'

    imgr_value = fields.Float('Valor IMGR', default=0)
