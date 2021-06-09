# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Employee Ux',
    'version': '13.0.1.0',
    'description': 'Some Ux improvements to the hr_employee ux to make the views more readeable.',
    'summary': 'Some Ux improvements to the hr_employee ux to make the views more readeable.',
    'author': 'Nimarosa',
    'website': 'www.nimarosa.com',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr',
        'hr_contract',
        'hr_attendance',
        'hr_attendance_autoclose',
        'hr_employee_age',
        'hr_employee_identification',
        'hr_employee_service'
    ],
    'data': [
        'views/hr_employee.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
