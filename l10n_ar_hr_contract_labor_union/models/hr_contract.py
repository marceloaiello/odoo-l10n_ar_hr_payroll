from odoo import api, fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'
    cct_id = fields.Many2one(comodel_name='hr.labor_union', string='C.C.T / Sindicato')
    cct_category_id = fields.Many2one(comodel_name='hr.labor_union.category', string='Categoria C.C.T')


