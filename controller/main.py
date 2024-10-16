from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response
import json

class SaleOrderAPIController(http.Controller):

    @http.route('/api/create_sale_order', type='http', auth='public', methods=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        kwargs = request.get_json_data()
        partner_id = kwargs.get('partner_id')
        order_lines = kwargs.get('order_lines')

        # Validate partner_id
        if not partner_id:
            return {"error": "partner_id is required."}, 400
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return {"error": f"Partner with ID {partner_id} does not exist."}, 404

        # Validate order_lines
        if not order_lines or not isinstance(order_lines, list):
            return {"error": "order_lines must be a non-empty list."}, 400

        sale_order_lines = []
        for line in order_lines:
            product_id = line.get('product_id')
            quantity = line.get('quantity', 1)
            price_unit = line.get('price_unit', 0.0)

            # Validate product_id
            product = request.env['product.product'].sudo().browse(product_id)
            if not product.exists():
                return {"error": f"Product with ID {product_id} does not exist."}, 404

            # Prepare order line data
            sale_order_lines.append((0, 0, {
                'product_id': product_id,
                'product_uom_qty': quantity,
                'price_unit': price_unit,
            }))

        # Create the sale order (quotation)
        try:
            sale_order = request.env['sale.order'].sudo().create({
                'partner_id': partner_id,
                'order_line': sale_order_lines,
            })
        except Exception as e:
            return {"error": str(e)}, 500

        # Return the success response
        data =  {
            "success": True,
            "message": "Sale order created successfully",
            "sale_order_id": sale_order.id,
            "sale_order_name": sale_order.name,
        }
        return request.make_response(http.json.dumps(data),
            headers={'Content-Type': 'application/json'})
    


