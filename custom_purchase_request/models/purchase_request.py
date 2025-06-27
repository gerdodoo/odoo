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
        store=True, readonly=True, index=True, tracking=True
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

@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        # Asignar número de secuencia
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or _('Nuevo')
        
        # --- LÓGICA DE DEPARTAMENTO MODIFICADA Y MÁS ROBUSTA ---
        # Si el departamento no viene en los valores y hay un solicitante...
        if not vals.get('department_id') and vals.get('requester_id'):
            # Obtenemos el ID del usuario solicitante
            user_id = vals.get('requester_id')
            
            # Buscamos explícitamente en el modelo 'hr.employee' al empleado
            # que esté vinculado con este user_id.
            # Usamos sudo() para buscar en todas las compañías sin problemas de permisos,
            # ya que la regla del empleado podría restringir la visibilidad.
            # `search_count` es más rápido si solo queremos verificar.
            # Vamos a buscar directamente el empleado.
            
            Employee = self.env['hr.employee']
            # Buscamos sin restricciones de compañía para encontrar el registro del empleado donde sea que esté.
            employee = Employee.search([('user_id', '=', user_id)], limit=1)
            
            if employee and employee.department_id:
                # Si encontramos un empleado y tiene un departamento, lo asignamos.
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
