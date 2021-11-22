# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payroll Employee Benefit',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'author': "Nimarosa",
    'website': 'https://nimarosa.dev',
    'depends': [
        'payroll',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/hr_contract.xml',
        'views/hr_employee_benefit_category.xml',
        'views/hr_employee_benefit_rate.xml',
        'views/hr_salary_rule.xml',
        'views/hr_payslip.xml',
    ],
    'installable': True,
}
