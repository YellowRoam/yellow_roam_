import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import stripe
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Flask app setup
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, origins=["https://yellowroam.github.io"])
# Stripe keys (loaded securely)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
YOUR_DOMAIN = os.getenv("YOUR_DOMAIN", "http://localhost:5000")

# In-memory storage for RoamReach emails
email_log = []

# Home route
@app.route("/")
def home():
    return render_template("OriginalLayout.html")
# Prompt route
@app.route("/prompt", methods=["POST"])
def prompt():
    user_input = request.form.get("user_input")
    if not user_input:
        return "Please enter a valid question.", 400
    # Logic to handle the prompt (basic placeholder response for now)
    logging.info(f"Prompt received: {user_input}")
    return f"You asked: {user_input} — A detailed response will be generated here."

# Email signup route
@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    if email:
        email_log.append(email)
        logging.info(f"RoamReach signup received: {email}")
        return "Thanks for signing up for RoamReach!"
    return "Please enter a valid email address.", 400

# Subscription handling route
@app.route("/subscribe/<plan>")
def subscribe(plan):
    price_lookup = {
        "explorer": os.getenv("PRICE_EXPLORER"),
        "pioneer": os.getenv("PRICE_PIONEER"),
        "trailblazer": os.getenv("PRICE_TRAILBLAZER")
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
        logging.error(f"Stripe checkout error: {e}")
        return "Error processing your subscription.", 500

# Health check route for Render
@app.route("/status")
def status():
    return "YellowRoam backend is running!", 200

# Main entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import request, jsonify

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    data = request.get_json()
    message = data.get("message")
    return jsonify({ "reply": f"You said: {message}" })
