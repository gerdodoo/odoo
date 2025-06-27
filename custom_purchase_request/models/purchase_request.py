from odoo import models, fields, api, _

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Solicitud de Compra Interna'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    # ... (aquí van todos tus campos: name, requester_id, etc.) ...
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
        store=True, index=True, tracking=True
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

    # --- MÉTODOS PARA EL FLUJO DE APROBACIÓN ---
    def action_submit(self):
        self.write({'state': 'to_approve'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    # --- MÉTODO CREATE CON LA LÓGICA DE SECUENCIA ---
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or _('Nuevo')
        
        return super(PurchaseRequest, self).create(vals_list)
