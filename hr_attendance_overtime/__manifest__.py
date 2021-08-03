# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Overtime',
    'version': '13.0.1.0.0',
    'description': 'This module adds overtime calculation funcionality to hr_attendance',
    'summary': 'This module adds overtime calculation funcionality to hr_attendance',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/hr/hr_attendance_overtime',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr_attendance'
    ],
    'data': [
        'views/hr_overtime.xml',
        'views/hr_attendance',
        'views/menus.xml',
        'data/hr_overtime_scheduler.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
