
from odoo import _, api, fields, models
from odoo.exceptions import UserError



class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.wizard'
    
    sale_id = fields.Many2one('sale.order',"Sale Id")
   
    def action_confirm_sale_order(self):
        self.sale_id.action_confirm()