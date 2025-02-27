# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Swathy K S (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api

class AccountMoveLine(models.Model):
    """Inherit model account move line for adding new fields"""
    _inherit = "account.move.line"

    product_image = fields.Binary(
        related="product_id.image_1920",
        string="Product Image",
        help="Product image"
    )

    analytic_account_code = fields.Char(
        string="Código Cuenta Analítica",
        compute="_compute_analytic_account_code",
        store=True
    )

    @api.depends('analytic_distribution')
    def _compute_analytic_account_code(self):
        for line in self:
            if line.analytic_distribution:
                analytic_ids = list(line.analytic_distribution.keys())  # Extrae los IDs de cuentas analíticas
                if analytic_ids:
                    analytic_account = self.env['account.analytic.account'].browse(int(analytic_ids[0]))  # Obtiene la cuenta analítica
                    line.analytic_account_code = analytic_account.code if analytic_account else ''
                else:
                    line.analytic_account_code = ''
            else:
                line.analytic_account_code = ''
