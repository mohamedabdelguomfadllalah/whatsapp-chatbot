from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)
import os
if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    print("Gunicorn detected, Flask app is ready!")


# استخدم متغيرات البيئة لمفاتيح OpenAI و Twilio
openai.api_key = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWIL
