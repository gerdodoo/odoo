# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Solicitud de Compra Interna'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    name = fields.Char(
        'Referencia', required=True, copy=False, readonly=True,
        default=lambda self: _('Nuevo'), tracking=True
    )
    requester_id = fields.Many2one(
        'res.users', string='Solicitante', required=True, index=True,
        default=lambda self: self.env.user, tracking=True
    )
    department_id = fields.Many2one(
        'hr.department', string='Departamento Solicitante',
        store=True, index=True, tracking=True # <-- Se eliminó readonly=True
    )
    company_id = fields.Many2one(
        'res.company', string='Compañía', required=True,
        default=lambda self: self.env.company
    )
    request_date = fields.Date(
        'Fecha de Solicitud', default=fields.Date.context_today,
        required=True, tracking=True
    )
    request_line_ids = fields.One2many(
        'purchase.request.line', 'request_id',
        string='Líneas de Solicitud', copy=True
    )
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('to_approve', 'Para Aprobar'),
        ('approved', 'Aprobado'),
        ('done', 'Realizado'),
        ('rejected', 'Rechazado'),
    ], string='Estado', default='draft', tracking=True)

# En models/purchase_request.py

# En models/purchase_request.py

@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        # Asignar número de secuencia
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or _('Nuevo')
        
        # --- LÓGICA DE DEPARTAMENTO CON SUDO() PARA BYPASS DE REGLAS DE ACCESO ---
        if not vals.get('department_id') and vals.get('requester_id'):
            user_id = vals.get('requester_id')
            
            # Usamos sudo() para que la búsqueda se ejecute con permisos de administrador.
            # Esto permite encontrar al empleado incluso si está en una compañía diferente
            # a la que el usuario está usando actualmente, saltando las reglas de acceso
            # que podrían impedirlo.
            
            Employee = self.env['hr.employee'].sudo() # <-- ¡LA CLAVE ESTÁ AQUÍ!
            
            employee = Employee.search([('user_id', '=', user_id)], limit=1)
            
            if employee and employee.department_id:
                vals['department_id'] = employee.department_id.id
    
    return super(PurchaseRequest, self).create(vals_list)

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Línea de Solicitud de Compra'

    request_id = fields.Many2one(
        'purchase.request', string='Solicitud de Compra', required=True, ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product', string='Producto', required=True,
        domain="[('purchase_ok', '=', True)]"
    )
    description = fields.Text('Descripción', required=True)
    quantity = fields.Float('Cantidad', default=1.0, required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', string='Unidad de Medida',
        related='product_id.uom_po_id' # Unidad de medida de compra del producto
    )
