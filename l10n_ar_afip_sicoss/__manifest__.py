# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Payroll - Localizacion Argentina',
    'version': '13.0.1.0',
    'description': 'Adds afip fields to the hr and payroll modules to support import/export',
    'summary': 'Adds afip fields to the hr and payroll modules to support import/export',
    'author': 'Nimarosa',
    'website': 'https://github.com/nimarosa/hr',
    'license': 'LGPL-3',
    'category': 'Payroll, Human Resources',
    'depends': [
        'hr', 'hr_contract', 'payroll', 'hr_contract_labor_union', 'hr_employee_ux', 'hr_contract_ux'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/afip_fields_views.xml',
        'views/menus.xml',
        'data/tablas_afip.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
