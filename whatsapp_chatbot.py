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
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    reply = resp.message()

    try:
        response = client.chat.completions.create(
    model="gpt-4o",  # استخدم النموذج المدفوع
    messages=[{"role": "user", "content": incoming_msg}]
)

        bot_reply = response.choices[0].message.content
    
    except openai.AuthenticationError:
        bot_reply = "❌ خطأ: مفتاح OpenAI غير صالح أو منتهي الصلاحية. تحقق منه في Render."
    except openai.RateLimitError:
        bot_reply = "🚨 عذرًا، لقد تجاوزت الحد المسموح به من الطلبات. حاول لاحقًا."
    except Exception as e:
        bot_reply = f"❌ حدث خطأ غير متوقع: {str(e)}"

    reply.body(bot_reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
