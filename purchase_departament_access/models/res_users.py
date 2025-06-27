from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_department_ids = fields.Many2many(
        'hr.department',
        string='Allowed Departments',
        help='Departments this user can access purchase orders for',
    )
