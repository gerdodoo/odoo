from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('phone')
    def validate_phone(self):
        for rec in self:
            if rec.phone:
                # Expresión regular para validar solo números, permitiendo el símbolo + al inicio
                if not re.fullmatch(r"^\+?[0-9]+$", rec.phone):
                    raise ValidationError('El número de teléfono solo puede contener números y opcionalmente empezar con "+".')

                # Verificar longitud mínima
                if len(rec.phone) < 6:
                    raise ValidationError('El número de teléfono debe tener al menos 6 dígitos.')
