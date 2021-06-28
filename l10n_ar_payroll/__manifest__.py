# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Configuracion de Payroll AFIP ARG (l10n_ar)',
    'version': '13.0.1.0',
    'description': 'Configuracion de Payroll - Localizacion Argentina',
    'summary': 'Configuracion de Payrol- Localizacion Argentina',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/nimarosa/hr',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr', 'hr_contract', 'payroll', 'l10n_ar_afip_sicoss', 'l10n_ar_payroll_payslip_report'
    ],
    'data': [
        'data/hr_contribution_register.xml', 'data/hr_salary_rule.xml', 'data/hr_salary_rule_category.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
