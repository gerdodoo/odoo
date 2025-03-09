from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPickingWizard(models.TransientModel):
    _name = 'stock.picking.wizard'
    _description = 'Wizard for Stock Picking'

    picking_type_id = fields.Many2one(
        'stock.picking.type', string='Operation Type', required=True,
        domain=[('code', '=', 'outgoing')]
    )
    location_id = fields.Many2one('stock.location', string='Source Location', required=True)
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', required=True)
    picking_id = fields.Many2one('stock.picking', string='Stock Picking', readonly=True)
    
    move_line_ids = fields.One2many('stock.picking.wizard.line', 'wizard_id', string='Products')

    def action_create_picking(self):
        if not self.move_line_ids:
            raise UserError('Please add at least one product to move.')
        
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'move_ids_without_package': [(0, 0, {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_id.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
            }) for line in self.move_line_ids],
        })
        
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate()
        
        self.picking_id = picking.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': picking.id,
            'target': 'current',
        }

class StockPickingWizardLine(models.TransientModel):
    _name = 'stock.picking.wizard.line'
    _description = 'Stock Picking Wizard Line'

    wizard_id = fields.Many2one('stock.picking.wizard', string='Wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
