# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payroll Argentina - l10n_ar',
    'version': '14.0.3.0.0',
    'description': 'Adaptacion del modulo payroll para Localizacion Argentina.',
    'summary': 'Configuracion y adaptaicones modulo payroll para Argentina.',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/nimarosa/hr/l10n_ar_payroll',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'depends': [
        'base',
        'hr_contract',
        'hr_attendance',
        'hr_holidays',
        'hr_holidays_public',
        'payroll',
        'l10n_ar',
        'l10n_ar_hr_contract_labor_union',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/tablas_afip_sicoss.xml',
        'views/afip_fields_views.xml',
        'views/menus.xml',
        'views/hr_contract.xml',
        'data/hr_contribution_register.xml',
        'data/hr_leaves.xml',
        'data/hr_salary_rule_category.xml',
        'data/hr_salary_rule.xml',
        'data/hr_payroll_structure.xml',
        'data/hr_contract_advantage_template.xml',
        'report/l10n_ar_payslip_report_template.xml',
        'report/l10n_ar_payslip_report.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
