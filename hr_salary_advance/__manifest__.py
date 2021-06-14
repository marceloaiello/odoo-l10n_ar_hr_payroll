# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Salary Advance',
    'version': '13.0.1.1.0',
    'summary': 'Advance Salary in HR',
    'description': """
        Helps you to manage Advance Salary Request of your company's staff.
        """,
    'category': 'Human Resources',
    'author': "Nimarosa",
    'maintainer': "httpsNimarosa",
    'website': 'https://github.com/nimarosa/hr',
    'depends': [
        'hr', 'account', 'hr_contract'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/salary_advance.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

