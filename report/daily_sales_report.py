from odoo import models, api

class DailySalesReport(models.AbstractModel):
    _name = "report.odoo_multi_tasks.report_template"
    _description = "Daily Sales Report Template"

    @api.model
    def _get_report_values(self, docids, data=None):
        start_date = data.get('start')
        end_date = data.get('end')

        sales_orders = self.env['sale.order'].search([
            ('date_order', '>=', start_date),
            ('date_order', '<=', end_date),
            ('state', 'in', ['sale', 'done'])
        ])

        report_data = []
        for order in sales_orders:
            report_data.append({
                'order_no': order.name,
                'date': order.date_order.strftime('%Y-%m-%d'),
                'customer': order.partner_id.name,
                'amount': order.amount_total,
            })

        return {
            'doc_ids': docids,
            # 'doc_model': 'sale.order',
            'data': data,
            'orders': report_data,
            'start_date': start_date,
            'end_date': end_date,
        }
