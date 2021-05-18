# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Argentina UX',
    'version': '13.01.0',
    'description': 'UX Modifications for the HR Module - Argentina',
    'summary': 'This module contains the modifications to make the HR UX acording to Argentina',
    'author': 'Nimarosa',
    'website': 'www.nimarosa.com',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr',
        'hr_payroll',
        'base'
    ],
    'data': [
        'views/hr_contract.xml'
    ],
    'auto_install': True,
    'auto_install': False,
    'application': False,
}
