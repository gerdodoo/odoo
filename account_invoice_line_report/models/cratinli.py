from odoo import models, fields

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Cuenta Analítica",
    )

    def _select(self):
        return super()._select() + ", line.analytic_account_id as analytic_account_id"

    def _group_by(self):
        return super()._group_by() + ", line.analytic_account_id"
