# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'AFIP SICOSS - l10n_ar',
    'version': '13.0.1.0',
    'description': 'Añade campos, datos y funcionalidades para integracion payroll con AFIP SICOSS.',
    'summary': 'Añade campos, datos y funcionalidades para integracion payroll con AFIP SICOSS.',
    'author': 'Nimarosa',
    'website': 'https://github.com/nimarosa/hr',
    'license': 'LGPL-3',
    'category': 'Payroll, Human Resources',
    'depends': [
        'hr_contract'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/afip_fields_views.xml',
        'views/menus.xml',
        'data/tablas_afip.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
