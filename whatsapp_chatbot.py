import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# استدعاء مفتاح API من متغيرات البيئة
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def get_openai_response(user_message):
    """ إرسال الرسالة إلى OpenAI API والحصول على رد """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",  # استخدم GPT-4o أو أي نموذج لديك
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "عذرًا، هناك مشكلة في الاتصال بـ OpenAI. حاول لاحقًا!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """ استقبال الرسائل من Twilio والرد عليها """
    incoming_msg = request.values.get("Body", "").strip()
    
    if not incoming_msg:
        reply = "الرجاء إرسال رسالة نصية!"
    else:
        reply = get_openai_response(incoming_msg)

    response = MessagingResponse()
    response.message(reply)

    return str(response)

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Chatbot with OpenAI is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
