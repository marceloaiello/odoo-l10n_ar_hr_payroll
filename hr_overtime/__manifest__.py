# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Overtime',
    'version': '14.0.2.0.0',
    'description': 'Crea el modelo hr_overtime que opera con hr_attendance para generar horas extras en base a la asistencia.',
    'summary': 'hr_overtime permite calcular horas extras a partir de los registros de asistencias, o manualmente.',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/hr/hr_overtime',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr_attendance'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_overtime.xml',
        'views/hr_overtime_type.xml',
        'views/menus.xml',
        'data/hr_overtime_scheduler.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
