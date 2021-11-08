# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR & Payroll UX - Argentina',
    'version': '14.0.4.0.0',
    'description': 'Modificaciones de UI para adaptar el sistema al uso en Argentina',
    'summary': 'Mejoras de UI para el sistema Payroll en Argentina.',
    'author': 'Nimarosa',
    'website': 'https://github.com/nimarosa/hr/l10n_ar_hr_ux',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'base',
        'hr_contract',
        'payroll',
    ],
    'data': [
        'views/hr_employee.xml',
        'views/hr_contract.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
