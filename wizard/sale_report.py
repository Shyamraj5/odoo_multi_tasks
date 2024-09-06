
from odoo import _, api, fields, models
from odoo.exceptions import UserError



class SaleDailyReportPdf(models.TransientModel):
    _name = 'sale.order.report.pdf'
    

    from_date = fields.Date(string="Start Date")
    to_date = fields.Date(string="End Date")