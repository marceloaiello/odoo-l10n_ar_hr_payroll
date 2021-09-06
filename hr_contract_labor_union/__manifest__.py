# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Labor Union (Sindicatos) - Argentina',
    'version': '14.0.1.0.0',
    'description': 'Añade la funcionalidad de manejar sindicatos y su integracion con hr_payroll.',
    'summary': 'Permite manejar sindicatos en odoo de acuerdo a la ley Argntina.',
    'author': 'Nimarosa',
    'website': 'https://github.com/nimarosa/hr/hr_contract_labor_union',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'hr_contract'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_labor_union.xml',
        'views/hr_labor_union_category_price.xml',
        'views/hr_contract.xml',
        'views/hr_labor_union_menus.xml',
        'wizard/hr_labor_union_category_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
