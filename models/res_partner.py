from odoo import models, fields,api,_


class ResPartner(models.Model):
    _inherit = "res.partner"

    total_sales = fields.Float(string="Total sales",compute="_compute_total")

    @api.depends('sale_order_ids')
    def _compute_total(self):
        for partner in self:
            total_sale = sum(order.amount_total for order in partner.sale_order_ids)
            partner.total_sales = total_sale
