from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    ubicacion = fields.Selection([
        ('PANTITLAN', 'Pantitlan'),
        ('TEXCOCO', 'Texcoco'),
        ('COACALCO', 'Coacalco'),
        ('LAGO_LADOGA', 'Lago Ladoga'),
        ('GANADEROS', 'Ganaderos'),
        ('TOLUCA', 'Toluca'),
        ('QUERETARO', 'Queretaro'),
        ('CELAYA', 'Celaya'),
        ('GUADALAJARA', 'Guadalajara'),
        ('PUERTO_VALLARTA', 'Puerto Vallarta'),
        ('AGUASCALIENTES', 'Aguascalientes'),
        ('PUEBLA', 'Puebla'),
    ], string='Ubicación')

    distrito_id = fields.Many2one('res.distrito', string='Distrito')

    @api.onchange('ubicacion')
    def _onchange_ubicacion(self):
        mapping = {
            'PANTITLAN': ['NEZA', 'AEROPUERTO', 'LOS_REYES'],
            'TEXCOCO': ['TEXCOCO'],
            'COACALCO': ['TULTITLAN', 'HUEHUETOCA'],
            'LAGO_LADOGA': ['SANTA_FE', 'CONDESA'],
            'GANADEROS': ['LAS_AGUILAS', 'PEDREGAL', 'TLALPAN'],
            'TOLUCA': ['LERMA', 'METEPEC'],
            'QUERETARO': ['QUERETARO'],
            'CELAYA': ['CELAYA'],
            'GUADALAJARA': ['GUADALAJARA'],
            'PUERTO_VALLARTA': ['PUERTO_VALLARTA'],
            'AGUASCALIENTES': ['AGUASCALIENTES'],
            'PUEBLA': ['ANGELOPOLIS'],
        }
        distritos = mapping.get(self.ubicacion, [])
        return {'domain': {'distrito_id': [('name', 'in', distritos)]}}

    @api.constrains('ubicacion', 'distrito_id')
    def _check_distrito_valido(self):
        mapping = {
            'PANTITLAN': ['NEZA', 'AEROPUERTO', 'LOS_REYES'],
            'TEXCOCO': ['TEXCOCO'],
            'COACALCO': ['TULTITLAN', 'HUEHUETOCA'],
            'LAGO_LADOGA': ['SANTA_FE', 'CONDESA'],
            'GANADEROS': ['LAS_AGUILAS', 'PEDREGAL', 'TLALPAN'],
            'TOLUCA': ['LERMA', 'METEPEC'],
            'QUERETARO': ['QUERETARO'],
            'CELAYA': ['CELAYA'],
            'GUADALAJARA': ['GUADALAJARA'],
            'PUERTO_VALLARTA': ['PUERTO_VALLARTA'],
            'AGUASCALIENTES': ['AGUASCALIENTES'],
            'PUEBLA': ['ANGELOPOLIS'],
        }
        for record in self:
            if record.distrito_id and record.ubicacion:
                distritos_validos = mapping.get(record.ubicacion, [])
                if record.distrito_id.name not in distritos_validos:
                    raise ValidationError(
                        f"El distrito '{record.distrito_id.name}' no es válido para la ubicación '{record.ubicacion}'."
                    )
