from odoo import models, fields

class ResDistrito(models.Model):
    _name = 'res.distrito'
    _description = 'Distrito'

    name = fields.Char(string='Nombre', required=True)
