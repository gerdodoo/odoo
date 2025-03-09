# -*- coding: utf-8 -*-
###############################################################################
#
# Cybrosys Technologies Pvt. Ltd.
#
# Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
# Author: Ayana KP (odoo@cybrosys.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, api, fields, _, SUPERUSER_ID
from odoo.exceptions import UserError


class CarWorkshop(models.Model):
    """ Model for car workshop management """
    _name = 'car.workshop'
    _description = "Car Workshop"
    _inherit = ['mail.thread']

    def action_open_stock_picking_wizard(self):
        """ Opens the stock picking wizard """
        return {
            'name': _('Generate Stock Picking'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_workshop_id': self.id,
                'default_picking_type_id': self.env['stock.picking.type'].search([], limit=1).id,
                'default_location_id': self.env['stock.location'].search([('usage', '=', 'internal')], limit=1).id,
                'default_location_dest_id': self.env['stock.location'].search([('usage', '=', 'customer')], limit=1).id,
            },
        }

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Ensures all stages appear in the Kanban view """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _default_stage_id(self):
        """ Fetches the first available stage """
        return self.env['worksheet.stages'].search([], limit=1)

    # Fields
    name = fields.Char(string='Title', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    vehicle_id = fields.Many2one('vehicle.details', string='Vehicle', index=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Assigned to', default=lambda self: self.env.user, tracking=True)
    active = fields.Boolean(string='Active', default=True)
    partner_id = fields.Many2one('res.partner', string='Customer', related='vehicle_id.partner_id')
    priority = fields.Selection([('0', 'Normal'), ('1', 'High')], string='Priority', index=True, default='0')
    description = fields.Html(string='Description')
    date_start = fields.Datetime(string='Starting Date', default=fields.Datetime.now, index=True)
    date_end = fields.Datetime(string='Ending Date', index=True)
    date_assign = fields.Date(string='Assigning Date', default=fields.Date.today, index=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    stage_id = fields.Many2one('worksheet.stages', string='Stage', ondelete='restrict', tracking=True, index=True,
                               default=_default_stage_id, group_expand='_read_group_stage_ids', copy=False)
    state = fields.Selection([
        ('waiting', 'Ready'),
        ('workshop_create_invoices', 'Invoiced'),
        ('cancel', 'Invoice Canceled'),
    ], string='Status', readonly=True, default='waiting', tracking=True, index=True)
    invoice_count = fields.Integer(string="Invoice Count", compute='_compute_invoice_count')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('car.workshop') or _('New')
        return super().create(vals)

    @api.depends('planned_work_ids.work_cost', 'materials_ids.price')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.planned_work_ids.mapped('work_cost')) + sum(record.materials_ids.mapped('price'))

    def cancel(self):
        """ Sets state to cancel """
        self.state = 'cancel'

    def action_create_invoices(self):
        """ Creates an invoice for the workshop """
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_('Please select a Customer.'))
        if not self.planned_work_ids:
            raise UserError(_('Nothing to invoice, Plan a work.'))
        
        journal = self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.company_id.id)], limit=1)
        if not journal:
            raise UserError(_('No Sales Journal found for the company.'))

        invoice = self.env['account.move'].create({
            'ref': self.name,
            'partner_id': self.partner_id.id,
            'currency_id': self.company_id.currency_id.id,
            'journal_id': journal.id,
            'invoice_origin': self.name,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': work.name,
                'account_id': work.planned_work_id.property_account_income_id.id,
                'price_unit': work.work_cost,
                'quantity': 1,
                'product_id': work.planned_work_id.id,
            }) for work in self.planned_work_ids if work.is_completed],
        })

        self.state = 'workshop_create_invoices'
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'account.move',
            'view_mode': 'form',
            'target': 'current',
            'res_id': invoice.id,
        }

    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([('invoice_origin', '=', self.name)])
