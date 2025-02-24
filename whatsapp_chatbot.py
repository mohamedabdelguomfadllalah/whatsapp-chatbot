from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# 🔹 ضع مفاتيح API الخاصة بك هنا
openai.api_key = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# 🔹 وظيفة للتفاعل مع ChatGPT
def chat_with_gpt(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    return response["choices"][0]["message"]["content"].strip()

# 🔹 استقبال رسائل WhatsApp عبر Twilio
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    reply = resp.message()
    
    if incoming_msg:
        bot_reply = chat_with_gpt(incoming_msg)
        reply.body(bot_reply)
    else:
        reply.body("مرحبًا! كيف يمكنني مساعدتك؟")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
