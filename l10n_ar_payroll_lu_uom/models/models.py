# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import UserError
from datetime import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        # Call super function computation and append new values.
        res = super().get_inputs(contracts, date_from, date_to)

        # -- add imgr input - last gross salary -- #
        for contract in contracts:
            if contract.schedule_pay == 'bi-weekly' and 'UOM' in contract.cct_id.name:
                res.append(
                    {
                        "name": 'UOM IMGR - Bruto imponible periodos anteriores',
                        "code": 'UOMIMGRGROSS',
                        "contract_id": contract.id,
                        "amount": self._get_month_gross(contract, date_from)
                    }
                )

        return res

    @api.model
    def _get_month_gross(self, contract, date_from):
        amount = 0.00
        affected_payslips = self.env['hr.payslip'].search([
            ('employee_id', '=', contract.employee_id.id),
            ('date_from', '>=', date_from.replace(day=1)),
            ('date_to', '<=', date_from)])
        if len(affected_payslips) > 0:
            for payslip in affected_payslips:
                lines = payslip.details_by_salary_rule_category.filtered(lambda r: r.category_id.code in ['TGROSS', 'TNOREM', 'VAC931', 'EXT931'])
                for line in lines:
                    if line.category_id.code == 'TGROSS':
                        amount += line.total
                    if line.category_id.code == 'TNOREM':
                        amount += line.total
                    if line.category_id.code == 'VAC931':
                        amount -= line.total
                    if line.category_id.code == 'EXT931':
                        amount -= line.total
        return amount


class HrContractLaborUnionCategoryPrice(models.Model):
    _inherit = 'hr.labor_union.category.price'

    imgr_value = fields.Float('Valor IMGR', default=0)
