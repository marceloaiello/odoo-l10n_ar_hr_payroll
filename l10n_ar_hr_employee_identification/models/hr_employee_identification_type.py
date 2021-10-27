# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployeeIdentificationType(models.Model):
    _name = "hr.employee.identification.type"
    _description = "Identification Types for Employees"
    _order = "name"

    name = fields.Char(required=True)
