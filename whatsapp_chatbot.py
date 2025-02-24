from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# استخدام مفاتيح API المخزنة في البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Chatbot is running with ChatGPT integration!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()  # استلام رسالة المستخدم
    resp = MessagingResponse()
    reply = resp.message()

    try:
        # إرسال الرسالة إلى ChatGPT والحصول على الرد
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # يمكنك تغييره إلى "gpt-4" إذا كان لديك حق الوصول
            messages=[{"role": "user", "content": incoming_msg}]
        )
        
        bot_reply = response["choices"][0]["message"]["content"]
    
    except Exception as e:
        bot_reply = "عذرًا، هناك مشكلة في الاتصال بـ ChatGPT. حاول مرة أخرى لاحقًا!"

    reply.body(bot_reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
