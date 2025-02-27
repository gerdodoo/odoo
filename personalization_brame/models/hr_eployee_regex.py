import re
from odoo import models, api
from odoo.exceptions import ValidationError

# /^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$/

class HrEmployee(models.Model):
    _inherit = "hr.employee"  # 🔹 Heredamos el modelo de empleados

    @api.constrains("curp")
    def _check_curp(self):
        curp_regex = r"^[A-Z]{4}\d{6}[HM]{1}[A-Z]{5}[0-9A-Z]{2}$"
        for record in self:
            if record.curp and not re.match(curp_regex, record.curp):
                raise ValidationError("La CURP ingresada no es válida. Verifica su formato.")

