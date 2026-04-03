import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

BOT_TOKEN = '8679546848:AAGwAoOSaX0SdqNEpLG27TAsysQMZ02Mp40'
CHAT_ID = '1015078873'

def send_telegram_message(name, email, message):
    """Send contact form data to Telegram"""
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    # Format the message nicely
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text = f"""
📬 <b>New Contact Form Submission</b>

👤 <b>Name:</b> {name}
📧 <b>Email:</b> {email}
💬 <b>Message:</b>
{message}

⏰ <b>Timestamp:</b> {timestamp}
"""

    data = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

@app.route('/send-message', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()

        name = data.get('fullname', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not all([name, email, message]):
            return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

        result = send_telegram_message(name, email, message)

        if 'ok' in result and result['ok']:
            return jsonify({'status': 'success', 'message': 'Message sent successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send message'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)