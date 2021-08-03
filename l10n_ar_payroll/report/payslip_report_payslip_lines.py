# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class HrPayslipLine(models.Model):
    # This handles the case when we need to distinguish the diferent amount column in the payslip generation. So we create
    # 3 columns acording to the report columns. The other columns remain null for this case.
    # THIS IS ONLY FOR THE REPORTS, DONT USE IT FOR CALCULATIONS, USE CATEGORIES FOR THAT.
    _inherit = 'hr.payslip.line'

    total_haberes = fields.Float(
        compute='_compute_afip_totals', string='Monto Haberes', store=True)
    total_descuentos = fields.Float(
        compute='_compute_afip_totals', string='Monto Descuentos', store=True)
    total_no_remunerativo = fields.Float(
        compute='_compute_afip_totals', string='Monto No Remunerativo', store=True)

    @api.depends('total')
    def _compute_afip_totals(self):
        for record in self:
            if record.total and record.appears_on_payslip is True:
                if record.category_id.parent_id.code == "GROSS":
                    record.total_haberes = record.total
                elif record.category_id.parent_id.code == "DESC":
                    record.total_descuentos = record.total
                elif record.category_id.parent_id.code == "NOREM":
                    record.total_no_remunerativo = record.total
            else:
                pass
