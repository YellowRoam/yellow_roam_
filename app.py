import os
import json
import logging
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI  # ✅ New SDK import
from openai._httpx_client import SyncHttpxClientWrapper
import stripe
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# === Load environment variables ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# === Initialize clients ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

stripe.api_key = STRIPE_SECRET_KEY

# === Initialize Flask app ===
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# === Logging Setup ===
logging.basicConfig(filename="yellowroam.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# === Routes ===

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_prompt = data.get("prompt", "").strip()

        if not user_prompt:
            return jsonify({"error": "Prompt is required."}), 400

        logging.info(f"🟡 Received prompt: {user_prompt}")

        # Call OpenAI API (v1.3.9)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful Yellowstone travel assistant."},
                {"role": "user", "content": user_prompt}
            ]
        )

        reply = response.choices[0].message.content
        logging.info(f"🟢 Assistant response: {reply}")

        return jsonify({"response": reply})

    except Exception as e:
        logging.error("🔴 EXCEPTION TRIGGERED IN /api/chat")
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    try:
        data = request.json
        email = data.get("email", "").strip()

        if not email:
            return jsonify({"error": "Email is required."}), 400

        # Send email notification
        msg = MIMEText(f"New RoamReach signup: {email}")
        msg["Subject"] = "New RoamReach Subscriber"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        return jsonify({"success": True})

    except Exception as e:
        logging.error("🔴 EXCEPTION TRIGGERED IN /api/subscribe")
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/api/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.json
        price_id = data.get("priceId")

        if not price_id:
            return jsonify({"error": "Missing price ID"}), 400

        session = stripe.checkout.Session.create(
            success_url="https://yellowroam.com/success",
            cancel_url="https://yellowroam.com/cancel",
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
        )

        return jsonify({"url": session.url})

    except Exception as e:
        logging.error("🔴 EXCEPTION TRIGGERED IN /api/create-checkout-session")
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# === Run the app (for local testing only; Gunicorn is used in production) ===
if __name__ == "__main__":
    app.run(debug=True)
