# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payroll Fiscal Period',
    'version': '14.0.2.1.0',
    'description': 'Adds fiscal periods to payroll',
    'summary': 'Adds fiscal periods to payroll',
    'author': 'Nimarosa',
    'website': 'nimarosa.dev',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'depends': [
        'payroll'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/hr_period.xml',
        'views/hr_fiscalyear.xml',
        'views/hr_payslip.xml',
        'views/hr_payslip_line.xml',
        'views/hr_payslip_run.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
