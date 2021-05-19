# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Employee UX Customizations',
    'version': '13.0.1.0',
    'description': 'This module adds ux customizations to the hr_employee module and submodules to make forms and views more flexible.',
    'summary': 'Adds modifications to the ux of the hr_employee module.',
    'author': 'Nimarosa',
    'website': 'www.nimarosa.com.ar',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr'
    ],
    'data': [
        'views/hr_employee.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
