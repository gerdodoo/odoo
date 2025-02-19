# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author:  Sabeel B (Contact : odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Unique Sequence in maintenance',
    'version': '17.0.1.0.0',
    'category': 'maintenance',
    'summary': 'Sequence number for mantenimiento',
    'description': """Module helps to Setup sequence number of maintenance""",
    'author': 'Brame tec IA',
    'company': 'Brame Tec',
    'maintainer': 'Brame tec',
    'website': 'https://www.brame.com',
    'depends': ['maintenance'],
    'data': [
        'data/equipment_sequence.xml',
        'views/view_equipment_form.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
