from odoo import models, fields


class ResConfig(models.TransientModel):
    _inherit = "res.config.settings"

    check_quick_sale_order = fields.Boolean("Quick Sale Order",default=True)
