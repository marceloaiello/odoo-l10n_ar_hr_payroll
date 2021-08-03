# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR UX Tweaks - Argentina',
    'version': '13.0.2.0',
    'description': 'Some Ux improvements ux to make the views more usable in Argentina.',
    'summary': 'Some Ux improvements to the hr_employee, hr_contract ux to make the views more usable in Argentina',
    'author': 'Nimarosa',
    'website': 'https://github.com/nimarosa/hr/l10n_ar_hr_ux',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr_contract'
    ],
    'data': [
        'views/hr_employee.xml', 'views/hr_contract.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
