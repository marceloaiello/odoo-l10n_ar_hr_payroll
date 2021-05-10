# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Contract Antiquity Date',
    'version': '13.0.1.0.0',
    'summary': 'Provides a field to enter the employee antiquity date and calculate antiquity.',
    'category': 'Human Resources',
    'author': 'Nimarosa',
    'maintainer': 'Nimarosa',
    'website': 'www.nimarosa.com',
    'license': 'AGPL-3',
    'contributors': [
        '',
    ],
    'depends': [
        'base',
        'hr',
    ],
    'external_dependencies': {
        'python': [
            '',
        ],
    },
    'data': [
        'views/hr_contract.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
