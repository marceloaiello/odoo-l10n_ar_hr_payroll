# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Employee Identification - Argentina',
    'version': '14.0.2.0.0',
    'description': 'Agrega campos de identificacion de empleados, DNI, CUIT, sus vencimientos y archivos para el legajo',
    'summary': 'Agrega campos de identificacion de empleados, DNI, CUIT, sus vencimientos y archivos para el legajo',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/nimarosa/l10n_ar_hr_payroll',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'base',
        'hr_contract',
    ],
    'data': [
        'data/hr_employee_identification.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_identification_type.xml',
        'views/hr_employee.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
