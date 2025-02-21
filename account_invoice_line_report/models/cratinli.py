from odoo import models, fields

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    analytic_account_id = fields.Text(
        comodel_name="analytic.distribution",
        string="Cuenta Analítica",
    )

    def _select(self):
        return super()._select() + ", line.analytic_distribution as analytic_distribution"

    def _group_by(self):
        return super()._group_by() + ", line.analytic_distribution"
