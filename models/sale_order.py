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
        buffer_days = -7  # You can change this to however many days before expiration you want
        
      
        expiring_quotations = self.search([
            
            ('validity_date', '>=', today),
        ])
        if expiring_quotations:
            product_table_html = """
                <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                    <thead>
                        <tr style="text-align:center">
                            <th>SL No</th>
                            <th>Quatation No</th>
                            <th>Date</th>
                            <th>Customer</th>
                            <th>AMount</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for rec in expiring_quotations:
                product_table_html += f"""
                    <tr style="text-align:right">
                        <td><td>
                        <td>{rec.name}</td>
                        <td>{rec.create_date}</td>
                        <td>{rec.partner_id.name}</td>
                        <td>{rec.amount_total}</td>
                    </tr>
                """
            product_table_html += """
                    </tbody>
                </table>
            """
            mail_template = self.env.ref('odoo_multi_tasks.quotation_expiring_email_template')
            try:
                mail_template.send_mail(
                                self.env.user.id,  # Sending as the current user
                                email_values={
                                    'email_to':"shinszoro69@gmail.com",
                                    'body_html': product_table_html,
                                })
            except Exception as e:
                    logger.error(f"Failed to send email{str(e)}")