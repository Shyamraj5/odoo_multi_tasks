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
    

    @http.route('/api/get_all_order',type='http',auth='public',methode=['GET'],csrf=False)
    def get_so(self,**kwargs):
        try:
            # Fetch all sale orders with necessary fields
            sale_orders = request.env['sale.order'].sudo().search([])
            sale_order_data = []
            
            for data in sale_orders:
                order_data = {
                    'id':data.id,
                    'type_name':data.type_name,
                    'name':data.name,
                    'partner_id':data.partner_id.id,
'                    date_order':data.date_order.strftime('%Y-%m-%d %H:%M:%S') if data.date_order else None,
                    'state': data.state,
                    'amount_total': data.amount_total,
                    'currency': data.currency_id.name,
                    'amount_tax':data.amount_tax,
                    'amount_untaxed':data.amount_untaxed,
                    
                }
                sale_order_data.append(order_data)

            response_data = {
                "success": True,
                "sale_orders": sale_order_data
            }
            return request.make_response(
                json.dumps(response_data),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            error_response = {
                "success": False,
                "error": str(e)
            }
            return request.make_response(
                json.dumps(error_response),
                headers={'Content-Type': 'application/json'}
            )
        

    @http.route('/api/get_by_partner_details',type='http',auth='public',methods=['POST'],csrf=False)
    def get_by_details(self,**kwargs):

        try:
            partner_name = kwargs.get('name')
            partner_phone = kwargs.get('phone')
            partner_email = kwargs.get('email')

            domain = []
            if partner_name:
                domain.append(('name', 'ilike', partner_name))
            if partner_phone:
                domain.append(('phone', 'ilike', partner_phone))
            if partner_email:
                domain.append(('email', 'ilike', partner_email))

            partners = request.env['res.partner'].sudo().search(domain)

            if not partners:
                return request.make_response(
                    json.dumps({"error": "No partner found with the provided details."}),
                    headers={'Content-Type': 'application/json'}
                )
            
            sale_orders = request.env['sale.order'].sudo().search([('partner_id', 'in', partners.ids)])
            
            sale_order_data = []
            for order in sale_orders:
                # Extract order line details
                order_lines = []
                for line in order.order_line:
                    line_data = {
                        'product_id': line.product_id.id,
                        'product_name': line.product_id.name,
                        'quantity': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'subtotal': line.price_subtotal
                    }
                    order_lines.append(line_data)

                # Prepare order data
                order_data = {
                    'id': order.id,
                    'name': order.name,
                    'partner_id': order.partner_id.id,
                    'partner_name': order.partner_id.name,
                    'date_order': order.date_order.strftime('%Y-%m-%d %H:%M:%S') if order.date_order else None,
                    'state': order.state,
                    'amount_total': order.amount_total,
                    'currency': order.currency_id.name,
                    'phone': order.partner_id.phone,
                    'order_lines': order_lines  # Include the order lines
                }
                sale_order_data.append(order_data)
                response_data = {
                "success": True,
                "sale_orders": sale_order_data
            }
            return request.make_response(
                json.dumps(response_data),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            # Handle any errors during the process
            error_response = {
                "success": False,
                "error": str(e)
            }
            return request.make_response(
                json.dumps(error_response),
                headers={'Content-Type': 'application/json'}
            )

