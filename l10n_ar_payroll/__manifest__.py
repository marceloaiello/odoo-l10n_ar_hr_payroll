# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payroll Argentina - l10n_ar',
    'version': '13.0.2.0.0',
    'description': 'Adaptacion del modulo payroll para Localizacion Argentina.',
    'summary': 'Configuracion y adaptaicones modulo payroll para Argentina.',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/nimarosa/hr/l10n_ar_payroll',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'depends': [
        'hr_contract',
        'hr_contract_labor_union',
        'hr_attendance',
        'hr_attendance_report_theoretical_time',
        'payroll'
    ],
    'data': [
        'views/views.xml',
        'data/hr_contribution_register.xml',
        'data/hr_leaves.xml',
        'data/hr_salary_rule_category.xml',
        'data/hr_salary_rule.xml',
        'data/hr_payroll_structure.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
