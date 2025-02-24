import os
import requests
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد مفتاح API الخاص بـ DeepSeek من متغيرات البيئة
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# دالة لاستدعاء DeepSeek API والحصول على الردود
def get_deepseek_response(user_message):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "عذرًا، هناك مشكلة في الاتصال بـ DeepSeek. حاول لاحقًا!"

# نقطة استقبال الرسائل من Twilio
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    
    if not incoming_msg:
        reply = "الرجاء إرسال رسالة نصية!"
    else:
        reply = get_deepseek_response(incoming_msg)

    # إنشاء استجابة Twilio
    response = MessagingResponse()
    response.message(reply)

    return str(response)

# الصفحة الرئيسية لاختبار الاتصال
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Chatbot with DeepSeek AI is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
