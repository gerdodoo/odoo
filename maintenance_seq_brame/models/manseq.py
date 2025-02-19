from odoo import models, fields, api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    sequence = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default=lambda self: self._get_next_sequence())

    @api.model
    def _get_next_sequence(self):
        return self.env['ir.sequence'].next_by_code('maintenance.equipment.form') or '/'
    
    @api.model
    def create(self, vals):
        if not vals.get('sequence'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.form')
        return super(MaintenanceEquipment, self).create(vals)
