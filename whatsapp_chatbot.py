from flask import Flask, request, jsonify, render_template
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
import requests
from langdetect import detect

app = Flask(__name__)

# تخزين الجلسات في الذاكرة
user_sessions = {}

# إعداد مفاتيح API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

openai.api_key = OPENAI_API_KEY

def detect_language(text):
    """اكتشاف لغة النص المدخل"""
    try:
        return detect(text)
    except:
        return "unknown"

def transcribe_audio(audio_url):
    """تحويل الصوت إلى نص باستخدام Whisper API"""
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {"file": audio_url, "model": "whisper-1"}
    response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("text", "لم أتمكن من تحليل الصوت.")
    else:
        return "حدث خطأ أثناء تحليل الصوت."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """التعامل مع رسائل واتساب"""
    user_id = request.values.get("From")
    user_message = request.values.get("Body")
    media_url = request.values.get("MediaUrl0")

    # إذا أرسل المستخدم تسجيلًا صوتيًا، نحوله لنص
    if media_url:
        user_message = transcribe_audio(media_url)

    # اكتشاف لغة الرسالة
    lang = detect_language(user_message)
    model = "gpt-4o" if lang == "ar" else "gpt-3.5-turbo"

    # بدء أو استرجاع جلسة المستخدم
    if user_id not in user_sessions:
        user_sessions[user_id] = [
            {"role": "system", "content": "أنت مساعد ذكي، حاول أن تكون دقيقًا ومنطقيًا في إجاباتك."}
        ]

    user_sessions[user_id].append({"role": "user", "content": user_message})

    # إرسال المحادثة إلى OpenAI
    response = openai.ChatCompletion.create(
        model=model,
        messages=user_sessions[user_id],
        temperature=0.7
    )

    bot_reply = response["choices"][0]["message"]["content"]
    user_sessions[user_id].append({"role": "assistant", "content": bot_reply})

    # إرسال الرد إلى واتساب
    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)

@app.route("/")
def index():
    """عرض صفحة بسيطة لمراقبة المحادثات"""
    return render_template("index.html", sessions=user_sessions)

if __name__ == "__main__":
    app.run(debug=True)
