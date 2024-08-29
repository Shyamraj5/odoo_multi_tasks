from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    
    image_1920 = fields.Binary(related='product_id.image_1920', readonly=False)