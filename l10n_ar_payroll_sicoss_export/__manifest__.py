# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payroll Export Sicoss - Argentina',
    'version': '14.0.1.2.2',
    'description': 'Agrega la funcionalidad de exportar el .txt para importacion en 931 SICOSS',
    'summary': 'Agrega la funcionalidad de exportar el .txt para importacion en 931 SICOSS',
    'author': 'Nimarosa',
    'website': 'nimarosa.dev',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'depends': [
        'payroll',
        'payroll_account',
        'payroll_period',
        'l10n_ar_payroll',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/payroll_sicoss_entry_views.xml',
        'views/payroll_sicoss_entry_item_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
