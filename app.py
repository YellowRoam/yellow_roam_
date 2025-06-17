import os
import json
import logging
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import stripe
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ✅ Import your custom logic function
from logic.chat_logic import process_prompt

# === Load environment variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# === Flask Setup ===
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# === Logging Setup ===
logging.basicConfig(filename="yellowroam.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# === Routes ===

@app.route("/")
def index():
    print("✅ Flask app reached /")
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        prompt = data.get("prompt", "").strip()
        tier = data.get("tier", "free")  # Defaults to 'free' if not passed

        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        logging.info(f"🟡 Incoming prompt: {prompt} | Tier: {tier}")

        # ✅ Custom logic processing
        processed_prompt = process_prompt(prompt, tier)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful Yellowstone travel assistant."},
                {"role": "user", "content": processed_prompt}
            ]
        )

        reply = response.choices[0].message["content"]
        logging.info(f"🟢 Assistant reply: {reply}")

        return jsonify({"response": reply})

    except Exception as e:
        logging.error("🔴 Chat route error")
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    try:
        data = request.json
        email = data.get("email", "").strip()

        if not email:
            return jsonify({"error": "Email is required."}), 400

        msg = MIMEText(f"New RoamReach signup: {email}")
        msg["Subject"] = "New RoamReach Subscriber"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        return jsonify({"success": True})

    except Exception as e:
        logging.error("🔴 Subscription error")
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
        logging.error("🔴 Stripe checkout error")
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# === Local development runner ===
if __name__ == "__main__":
    app.run(debug=True)
