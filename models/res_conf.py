from odoo import models, fields


class ResConfig(models.TransientModel):
    _inherit = "res.config.settings"

    check_quick_sale_order = fields.Boolean("Quick Sale Order",config_parameter="odoo_multi_tasks.check_quick_sale_order",default=False)



    def set_values(self):
        super(ResConfig, self).set_values()

        menu = self.env.ref('odoo_multi_tasks.sale_order_menu', raise_if_not_found=False)
        if menu:
           
            menu.write({'active': self.check_quick_sale_order})