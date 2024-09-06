from odoo import models, fields

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
    

    def open_confirm_wizard(self):
        self.ensure_one()  # Ensure that only one sale order is processed
        return {
            'name': 'Confirm Sale Order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
            },
        }
                        
    # #Finally Done


