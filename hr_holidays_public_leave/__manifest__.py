# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Holidays Override',
    'version': '14.0.1.1.0',
    'description': 'Automatically creates leaves for the public_holidays defined.',
    'summary': 'Automatically creates leaves for the public_holidays defined.',
    'author': 'Nimarosa',
    'website': 'nimarosa.dev',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr_holidays_public'
    ],
    'data': [
        'data/hr_leave_type.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
