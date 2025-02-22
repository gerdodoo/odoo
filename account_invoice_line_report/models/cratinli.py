from odoo import models, fields

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    analytic_distribution = fields.Text(
        string="Distribución Analítica",
        readonly=True
    )

    def _select(self):
        return super()._select() + ", line.analytic_distribution as analytic_distribution"
