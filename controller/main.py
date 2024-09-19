from odoo import http
import json
import logging

_logger = logging.getLogger(__name__)

class TelegramWebhookController(http.Controller):
    @http.route('/telegram/webhook/receiver', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **kwrgs):
        try:
            payload = json.loads(http.request.httprequest.data)
            _logger.info("Received payload: %s", payload)

            if 'message' in payload:
                message = payload['message']
                chat_id = message['chat']['id']
                text = message.get('text', '')
                
                if text == '/start':
                    response_text = "Welcome to the bot!"
                else:
                    response_text = "You said: {}".format(text)
                

                self.send_message(chat_id, response_text)

        except Exception as e:
            _logger.error("Error processing webhook: %s", str(e))
            return {'status': 'error', 'message': str(e)}

        return {'status': 'success'}

    def send_message(self, chat_id, text):
        """Send a message to a Telegram chat."""
        import requests
        token = 'YOUR_TELEGRAM_BOT_TOKEN'
        url = f"https://api.telegram.org/bot{6763457916:AAHidTHnMBSlNJiIfBNqfQYnf1cFcZ9WvzU}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            _logger.info("Message sent successfully")
        except requests.RequestException as e:
            _logger.error("Error sending message: %s", str(e))
