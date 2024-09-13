from venv import logger
from odoo import models, fields,api,_
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    is_quick_sale_order = fields.Boolean(string="Is quck sale order", default="False")




    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if self.is_quick_sale_order != True:
                if order.picking_ids:
                    order.picking_ids.button_validate()
                    order._create_invoices()
                    invoice_line = order.invoice_ids
                    for invoice in invoice_line:
                        invoice.action_post()
                        payment_vals = {
                            'partner_id': order.partner_id.id,
                            'payment_type': 'inbound',
                            'amount': invoice.amount_total,
                            'payment_method_id': invoice.payment_id.payment_method_id.id
                        }
                        payment = self.env['account.payment'].create(payment_vals)
                        payment.action_post()

                    payments = [{
                        'payment': payment,
                        'to_reconcile': invoice.line_ids,
                    }]
                    payment = self.env['account.payment.register']._reconcile_payments(payments)

            return res
            
    # #Finally Done
    @api.model
    def send_expiration_emails(self):
        today = fields.Date.today()
        buffer_days = 7
        
        expiring_quotations = self.search([
            ('validity_date', '>=', today),
            ('validity_date', '<=', fields.Date.add(today, days=buffer_days)),
            ('state', '!=', 'sale')
        ])
        
        if expiring_quotations:
            product_table_html = """
                <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
                    <thead style="background-color: #f2f2f2; color: #333; text-align: center;">
                        <tr>
                            <th style="border: 1px solid #ddd; padding: 8px;">SL No</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Quotation No</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Date</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Customer</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Amount</th>
                        </tr>
                    </thead>
                    <tbody style="background-color: #fff; color: #333;">
            """
            
            serial_number = 1   
            for rec in expiring_quotations:
                product_table_html += f"""
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{serial_number}</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{rec.name}</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{rec.create_date}</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{rec.partner_id.name}</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">{rec.amount_total}</td>
                    </tr>
                """
                serial_number += 1
            
            product_table_html += """
                    </tbody>
                </table>
            """
            
            mail_template = self.env.ref('odoo_multi_tasks.quotation_expiring_email_template')
            try:
                mail_template.send_mail(
                    self.env.user.id,  # Sending as the current user
                    email_values={
                        'email_to': "shyamrajkm5@gmail.com",
                        'body_html': product_table_html,
                    })
            except Exception as e:
                logger.error(f"Failed to send email {str(e)}")
