# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Labor Union - Argentina',
    'version': '13.0.2.0',
    'description': 'Adds labor union management to hr_contract and hr_payroll',
    'summary': 'This module allow to manage the Labor Union salary prices acording to Argentina Law',
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
        'data/lu_uom_metalurgicos.xml',
        'data/2021-2022-lu_uom_metalurgicos_rama3_art4.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
