from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# تحميل مفتاح OpenAI من المتغيرات البيئية
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ خطأ: مفتاح OpenAI غير موجود! تأكد من إضافته في Render.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)  # استخدام الطريقة الجديدة لإنشاء العميل

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Chatbot is running with ChatGPT integration!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", 
