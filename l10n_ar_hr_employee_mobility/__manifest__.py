# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Employee Mobility - Argentina',
    'version': '14.0.2.0.0',
    'description': 'Integra varios campos de datos de mobilidad para argentina. ',
    'summary': 'Integra varios campos de datos de mobilidad para argentina. Shell Flota.',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/nimarosa/l10n_ar_hr_payroll',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'base',
        'hr_contract',
    ],
    'data': [
        'views/hr_employee.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
