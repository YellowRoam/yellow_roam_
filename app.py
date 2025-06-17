# Clean and corrected version of the provided app.py structure
cleaned_app_py = """
import os
import json
import logging
import traceback
import smtplib
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from email.mime.text import MIMEText
import openai
import stripe

# === Load Environment Variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

print("✅ Environment loaded")
print("✅ OPENAI Key:", os.getenv("OPENAI_API_KEY"))
print("✅ STRIPE Key:", os.getenv("STRIPE_SECRET_KEY"))

# === Load All Logic Files ===
logic_folder = "logic"

def load_json_file(filename):
    path = os.path.join(logic_folder, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Core logic
intent_logic = load_json_file("intent.logic.json")
fallback_logic = load_json_file("fallback.logic.json")
system_prompt = load_json_file("system_prompt_multilingual.json")

# Language logic
language_logics = {}
for lang_code in ["en", "es", "fr", "hi"]:
    filename = f"{lang_code}.logic.json"
    language_logics[lang_code] = load_json_file(filename)

# Area-specific logic
area_logic = {
    "big_sky": load_json_file("big_sky.logic.json"),
    "bozeman": load_json_file("bozeman.logic.json"),
    "cody_cook_city": load_json_file("cody_cook_city.logic.json"),
    "ennis_virginia_city": load_json_file("ennis_virginia_city.logic.json"),
    "grand_teton": load_json_file("grand_teton.logic.json"),
    "jackson_driggs": load_json_file("jackson_driggs.logic.json"),
    "livingston_gardiner": load_json_file("livingston_gardiner.logic.json"),
    "red_lodge_beartooth": load_json_file("red_lodge_beartooth.logic.json"),
    "ski": load_json_file("ski_logic.logic.json")
}

# === Prompt Handling Logic ===
def handle_prompt(user_input, lang="en", area=None):
    clean_input = user_input.strip().lower()

    # Intent logic
    for intent in intent_logic:
        for pattern in intent["patterns"]:
            if pattern.lower() == clean_input:
                return intent["languages"].get(lang) or intent["languages"].get("en")

    # Language-specific logic
    lang_logic = language_logics.get(lang)
    if lang_logic:
        exact_match = lang_logic.get(user_input)
        if exact_match:
            return exact_match

    # Area-specific logic
    if area:
        area_file = area_logic.get(area)
        if area_file:
            area_match = area_file.get(user_input)
            if area_match:
                return area_match

    # Fallback logic
    fallback_list = fallback_logic["fallback_responses"].get(lang) or fallback_logic["fallback_responses"]["en"]
    return fallback_list[0]

# === Flask Setup ===
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# === Logging Setup ===
logging.basicConfig(filename='yellowroam.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# === Health Check Route ===
@app.route("/")
def home():
    return "YellowRoam API is up and running."

# === Core Chat Route Using Logic Files ===
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        lang = data.get("lang", "en")
        area = data.get("area", None)

        if not user_input:
            return jsonify({"error": "Prompt is required"}), 400

        reply = handle_prompt(user_input, lang=lang, area=area)
        return jsonify({"response": reply})

    except Exception as e:
        logging.error(f"Error in /api/chat: {traceback.format_exc()}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# === Stripe Webhook Handler ===
@app.route("/api/stripe/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        logging.info(f"✅ Stripe Event: {event['type']}")

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            logging.info(f"💰 Payment received for session {session.get('id')}")

        return '', 200

    except Exception as e:
        logging.error(f"Stripe webhook error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 400

# === Email Sending Route ===
@app.route("/api/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        subject = data.get("subject", "YellowRoam")
        message = data.get("message", "")
        recipient = data.get("to", os.getenv("ADMIN_EMAIL"))

        email = MIMEText(message)
        email["Subject"] = subject
        email["From"] = os.getenv("EMAIL_FROM")
        email["To"] = recipient

        with smtplib.SMTP(os.getenv("SMTP_SERVER"), 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            smtp.send_message(email)

        return jsonify({"status": "sent"})

    except Exception as e:
        logging.error(f"Error sending email: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# === Run for Local Dev Only ===
if __name__ == "__main__":
    app.run(debug=True)
"""

# Save the cleaned version
file_path = "/mnt/data/app_cleaned.py"
with open(file_path, "w") as f:
    f.write(cleaned_app_py)

file_path
