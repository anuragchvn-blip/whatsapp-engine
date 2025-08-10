from flask import Flask, render_template_string, request, redirect, url_for, flash
from whatsapp_bulk_sender import WhatsAppBulkSender
import threading

app = Flask(__name__)
app.secret_key = 'whatsapp-bulk-sender-demo'

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WhatsApp Bulk Sender (Web)</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f7f7; }
        .container { max-width: 500px; margin: 40px auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px #ccc; }
        h2 { color: #25D366; }
        textarea, input[type=text] { width: 100%; padding: 10px; margin: 8px 0 16px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #25D366; color: #fff; border: none; padding: 12px 30px; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #128C7E; }
        .flash { color: #d8000c; background: #ffd2d2; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>WhatsApp Bulk Sender</h2>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="flash">{{ messages[0] }}</div>
          {% endif %}
        {% endwith %}
        <form method="post">
            <label>Message:</label>
            <textarea name="message" rows="5" required placeholder="Type your message here..."></textarea>
            <label>Phone Numbers (comma separated):</label>
            <input type="text" name="phones" required placeholder="e.g. +911234567890, +919876543210">
            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>
'''

def send_bulk_async(contacts, message):
    sender = WhatsAppBulkSender()
    sender.send_bulk_messages(contacts, message)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        phones = request.form.get('phones', '').strip()
        if not message or not phones:
            flash('Please enter both message and phone numbers.')
            return redirect(url_for('index'))
        phone_list = [p.strip() for p in phones.split(',') if p.strip()]
        if not phone_list:
            flash('Please enter at least one phone number.')
            return redirect(url_for('index'))
        contacts = [{"phone": num, "name": "", "message": message} for num in phone_list]
        threading.Thread(target=send_bulk_async, args=(contacts, message)).start()
        flash(f'Sending to {len(contacts)} numbers. Please keep WhatsApp Web open.')
        return redirect(url_for('index'))
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
