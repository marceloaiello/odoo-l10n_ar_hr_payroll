# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrContractAdvantage(models.Model):
    """
    This linking with the payroll advantages templates and the contract module, provides the functionality to add "custom"
    values to a contract, so the user can choose the advantages linked to each contact, and this way we can assign
    (or leave default) the value for the advantage, and then use it in payroll salary rules to make calculations.

    Here we are doing the link between the hr_contract_advanges_templates that exists in the payroll module
    to the actual contract. This functionality was half implemented in the Payroll module from OCA, so here,
    we start implementing it for Argentina. So... TODO: Maybe pull request to OCA to add the uncompleted function.
    """

    _name = 'hr.contract.advantage'
    _description = 'Link contract advantages templates to payroll'

    contract_id = fields.Many2one('hr.contract', string='Contrato')
    contract_advantage_template_id = fields.Many2one('hr.contract.advantage.template', string='Concepto')
    code = fields.Char(string='Codigo', related='contract_advantage_template_id.code', readonly=True)
    use_default = fields.Boolean(string='¿Usar valor por defecto?', default=True)
    override_amount = fields.Float(string='Importe', related='contract_advantage_template_id.default_value', store=True)
    amount = fields.Float(compute='_compute_amount', string='Importe')
    advantage_lower_bound = fields.Float(
        string='Limite Inferior', related='contract_advantage_template_id.lower_bound')
    advantage_upper_bound = fields.Float(
        string='Limite Superior', related='contract_advantage_template_id.upper_bound')

    @api.depends('use_default', 'contract_advantage_template_id')
    def _compute_amount(self):
        for record in self:
            if record.use_default:
                if record.override_amount:
                    record.override_amount = 0.00
                record.amount = record.contract_advantage_template_id.default_value
            else:
                record.amount = record.override_amount

    @api.constrains('override_amount')
    def _check_bound_limits(self):
        for record in self:
            if record.override_amount:
                if record.override_amount != 0.00:
                    if record.override_amount > record.advantage_upper_bound:
                        raise ValidationError(
                            "El monto del parametro no puede ser mayor al limite superior asginado.")
                    elif record.override_amount < record.advantage_lower_bound:
                        raise ValidationError(
                            "El monto del parametro no puede ser menor al limite superior asginado.")

