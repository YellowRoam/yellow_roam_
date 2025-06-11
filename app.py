import os
import openai
from flask import Flask, render_template, request, redirect, url_for, jsonify
import stripe
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Load environment variables
load_dotenv()

# API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
YOUR_DOMAIN = os.getenv("YOUR_DOMAIN", "http://localhost:5000")

# Flask app setup
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, origins=[
    "https://yellowroam.github.io",
    "https://yellowroam.github.io/yellowroam-chat-ui",
])

# Logging
logging.basicConfig(level=logging.INFO)

# In-memory log
email_log = []

# Home route
@app.route("/")
def home():
    return render_template("OriginalLayout.html")

# Prompt route (OpenAI logic)
@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    data = request.get_json()
    message = data.get("message")
    logging.info(f"User message: {message}")

    if not message:
        return jsonify({"reply": "Please enter a valid question."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly Yellowstone travel assistant."},
                {"role": "user", "content": message}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return jsonify({"reply": "Sorry, something went wrong with the assistant."}), 500

# Email signup route
@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    if email:
        email_log.append(email)
        logging.info(f"Signup received: {email}")
        return "Thanks for signing up!"
    return "Please enter a valid email address.", 400

# Stripe plan selector
@app.route("/subscribe/<plan>")
def subscribe(plan):
    price_lookup = {
        "explorer": os.getenv("PRICE_EXPLORER"),
        "pioneer": os.getenv("PRICE_PIONEER"),
        "trailblazer": os.getenv("PRICE_TRAILBLAZER"),
    }
    price_id = price_lookup.get(plan.lower())
    if not price_id:
        return "Invalid plan selected.", 400

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            mode="subscription" if plan != "trailblazer" else "payment",
            success_url=YOUR_DOMAIN + "/?success=true",
            cancel_url=YOUR_DOMAIN + "/?canceled=true"
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        logging.error(f"Stripe error: {e}")
        return "Error processing your subscription.", 500

# Health check
@app.route("/status")
def status():
    return "YellowRoam backend is running!", 200
