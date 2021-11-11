# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Soporte Sindicato UOM (Argentina)',
    'version': '14.0.3.0.0',
    'description': 'Datos y adecuaciones para soportar el sindicato UOM en la localizacion Argentina de Payroll.',
    'summary': 'Agrega conceptos, categorias y precios para el sindicato UOM.',
    'author': 'Nimarosa',
    'website': 'https://www.github.com/nimarosa/odoo-l10n_ar_hr_payroll/l10n_ar_payroll_lu_uom',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'depends': [
        'l10n_ar_hr_contract_labor_union'
    ],
    'data': [
        'data/uom_salary_rules.xml',
        'data/uom_salary_structures.xml',
        'data/lu_uom_categories_rama3_art4.xml',
        'data/lu_uom_prices_rama3_art4.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
