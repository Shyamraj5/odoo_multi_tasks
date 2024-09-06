from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime

class SaleDailyReportPdf(models.TransientModel):
    _name = 'sale.order.report.pdf'
    
    from_date = fields.Date(string='Start Date', default=datetime.today())
    to_date = fields.Date(string='End Date')

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for record in self:
            if record.from_date and record.to_date and record.to_date < record.from_date:
                raise UserError('End Date must be greater than Start Date.')

    def print_pdf(self):
        data = {
            'start': self.from_date,
            'end': self.to_date,
        }
        return self.env.ref('odoo_multi_tasks.action_daily_sales_report_pdf').report_action(self, data=data)