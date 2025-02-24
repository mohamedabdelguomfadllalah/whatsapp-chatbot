from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# استخدام متغيرات البيئة لتخزين المفاتيح الحساسة
openai.api_key = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# الصفحة الرئيسية - لتأكيد أن السيرفر يعمل
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Chatbot is running!"

# Webhook لاستقبال الرسائل من WhatsApp عبر Twilio
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    reply = resp.message()

    if incoming_msg:
        bot_reply = "مرحبًا! كيف يمكنني مساعدتك؟"
        reply.body(bot_reply)

    return str(resp)

# تشغيل التطبيق على Render مع استخدام المنفذ الصحيح
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # ضبط المنفذ تلقائيًا بناءً على بيئة التشغيل
    app.run(host="0.0.0.0", port=port, debug=True)
