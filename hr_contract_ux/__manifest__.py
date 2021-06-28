# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Contract Ux',
    'version': '13.0.1.0',
    'description': 'Some Ux improvements to the hr_contract ux to make the views more readeable.',
    'summary': 'Some Ux improvements to the hr_contract ux to make the views more readeable.',
    'author': 'Nimarosa',
    'website': 'https://github.com/nimarosa/hr',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr',
        'hr_contract',
        'hr_contract_rate',
        'payroll',
        'payroll_account',
        'hr_contract_document',
        'hr_contract_labor_union'
    ],
    'data': ['views/hr_contract.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
