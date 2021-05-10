# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Labor Unions Tools - Argentina',
    'version': '13.0.1.0',
    'description': 'Adds labor union management to hr_contract and hr_payroll',
    'summary': 'Adds labor union management to hr_contract and hr_payroll',
    'author': 'Nimarosa',
    'website': 'www.nimarosa.com',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'base',
        'hr_contract',
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_labor_union.xml',
        'views/hr_contract.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
