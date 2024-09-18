from odoo import models, fields,api,_

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    
    image_1920 = fields.Binary(related='product_id.image_1920', readonly=False)


    @api.onchange("product_id")
    def check_price_list(self):
        res = super(SaleOrder, self)._onchange_product_id_warning()
        product_template_id = self.product_id.product_tmpl_id
        pricelist = self.order_id.pricelist_id
        if pricelist:
                product_in_pricelist = pricelist.item_ids.filtered(lambda item: item.product_tmpl_id == product_template_id)
                if product_template_id and not product_in_pricelist:
                    return {
                    'warning': {
                        'title': _("Warning"),
                        'message': _("This '%s' product is not available in the '%s' pricelist. Please update the pricelist to continue.") % (product_template_id.display_name, pricelist.name)
                    }
                }
        return res