import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import stripe
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# === Load Environment Variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# === Flask Setup ===
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# === Logging Setup ===
logging.basicConfig(filename='yellowroam.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# === Session Store for Free Tier ===
session_store = {}

# === Helper Functions ===
def load_location_data(location):
    filename = f"{location.lower().replace(' ', '_')}.json"
    path = os.path.join("yellowroam_data", filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def build_context_from_data(data):
    context = ""
    for section, items in data.items():
        context += f"\n\n{section.upper()}:\n"
        if isinstance(items, list):
            context += "\n".join(f"- {item}" for item in items)
        else:
            context += str(items)
    return context.strip()

def create_openai_prompt(location, user_input, tier="free"):
    location_data = load_location_data(location)
    data = {}

    if tier == "pro":
        data = location_data
    elif tier == "plus":
        for key in ["hikes", "dining", "hot_springs", "local_tips"]:
            if key in location_data:
                data[key] = location_data[key]
    elif tier == "basic":
        for key in ["hikes", "dining"]:
            if key in location_data:
                data[key] = location_data[key]
    else:
        data["message"] = "You're using the free version of YellowRoam. Upgrade to unlock more local insights."

    context = build_context_from_data(data)
    return f"You are YellowRoam, a helpful local travel guide. Use the data below to assist the user.\n\n{context}\n\nUser Question: {user_input}\n\nYour Answer:"

# === Routes ===
@app.route("/")
def home():
    return render_template("OriginalLayout.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    location = data.get("location", "").strip() or "yellowstone"
    tier = data.get("tier", "free")
    user_id = request.remote_addr

    logging.info(f"Chat request - Location: {location}, Tier: {tier}, Message: {user_input}, User: {user_id}")

    if tier == "free":
        user_session = session_store.get(user_id, {"count": 0})
        if user_session["count"] >= 3:
            return jsonify({
                "reply": "You've reached the limit for free questions. Please upgrade to continue exploring Yellowstone!"
            })
        else:
            user_session["count"] += 1
            session_store[user_id] = user_session

    try:
        prompt = create_openai_prompt(location, user_input, tier)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"reply": response.choices[0].message["content"].strip()})
    except Exception as e:
        logging.error(f"OpenAI error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    email = data.get("email", "").strip()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    logging.info(f"RoamReach signup received: {email}")

    try:
        msg = MIMEText(f"New RoamReach signup: {email}")
        msg["Subject"] = "New RoamReach Email Signup"
        msg["From"] = email
        msg["To"] = "heyday6159@gmail.com"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)
        return jsonify({"success": True})
    except Exception as e:
        logging.error(f"Email send failed: {str(e)}")
        return jsonify({"error": "Failed to send email"}), 500

@app.route("/api/checkout/<plan_id>", methods=["POST"])
def create_checkout_session(plan_id):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': plan_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=os.getenv("SUCCESS_URL"),
            cancel_url=os.getenv("CANCEL_URL"),
        )
        logging.info(f"Stripe session created for plan: {plan_id}")
        return jsonify({'checkout_url': session.url})
    except Exception as e:
        logging.error(f"Stripe error: {str(e)}")
        return jsonify({"error": str(e)}), 500
