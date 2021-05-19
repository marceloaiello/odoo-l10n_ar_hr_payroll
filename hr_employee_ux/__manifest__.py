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
        'base',
        'hr',
        'hr_attendance',
        'hr_attendance_autoclose',
        'hr_attendance_geolocation',
        'hr_attendance_reason',
        'hr_attendance_report_theoretical_time',
        'hr_contract',
        'hr_contract_rate',
        'hr_employee_age',
        'hr_employee_calendar_planning',
        'hr_employee_document',
        'hr_employee_identification',
        'hr_employee_medical_examination',
        'hr_employee_ppe',
        'hr_employee_relative',
        'hr_employee_service',
        'hr_employee_service_contract',
        'hr_org_chart',
        'hr_org_chart_overview'
    ],
    'data': [
        'views/hr_employee.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
