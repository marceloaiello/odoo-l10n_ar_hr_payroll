# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Soporte Sindicato ASIMRA (Argentina)',
    'version': '13.0.2.0.0',
    'description': 'Datos y adecuaciones para soportar el sindicato ASIMRA en la localizacion Argentina de Payroll.',
    'summary': 'Agrega conceptos, categorias y precios para el sindicato ASIMRA.',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/nimarosa/odoo-l10n_ar_hr_payroll/l10n_ar_payroll_lu_asimra',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'depends': [
        'l10n_ar_payroll'
    ],
    'data': [
        'data/asimra_salary_rules.xml',
        'data/asimra_salary_structure.xml',
        'data/lu_asimra_categories.xml',
        'data/lu_asimra_prices.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
