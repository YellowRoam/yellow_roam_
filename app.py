
from flask import Flask, render_template, request, redirect, url_for, jsonify
import stripe
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Stripe test keys (you'll replace with live keys later)
stripe.api_key = "sk_test_your_secret_key_here"
PUBLISHABLE_KEY = "pk_test_your_publishable_key_here"

# In-memory email log for RoamReach
email_log = []

# Sample itinerary logic (extensive placeholder)
def generate_itinerary(user_input):
    if "yellowstone" in user_input.lower():
        return {
            "title": "3-Day Yellowstone Itinerary",
            "days": [
                "Day 1: Enter through Gardiner, explore Mammoth Hot Springs and Lamar Valley",
                "Day 2: Visit Norris Geyser Basin, Grand Canyon of the Yellowstone",
                "Day 3: See Old Faithful, Grand Prismatic Spring, exit through West Yellowstone"
            ]
        }
    return {
        "title": "Sample Travel Itinerary",
        "days": [
            "Day 1: Arrival and orientation",
            "Day 2: Explore local highlights",
            "Day 3: Scenic departure"
        ]
    }

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/prompt", methods=["POST"])
def prompt():
    user_input = request.form.get("user_input", "")
    itinerary = generate_itinerary(user_input)
    return jsonify(itinerary)

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email", "")
    if email:
        email_log.append(email)
        logging.info(f"RoamReach signup received: {email}")
    return redirect(url_for("index"))

@app.route("/subscribe/<plan>", methods=["GET"])
def subscribe(plan):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{plan.capitalize()} Plan Subscription",
                    },
                    "unit_amount": 500 if plan == "explorer" else 0,
                    "recurring": {
                        "interval": "month",
                    },
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("index", _external=True),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        logging.error(f"Stripe error: {e}")
        return "An error occurred during checkout.", 500

@app.route("/success", methods=["GET"])
def success():
    return "<h1>Subscription successful!</h1><p>Thank you for supporting YellowRoam.</p>"

@app.errorhandler(404)
def not_found(e):
    return "<h1>404 - Page not found</h1>", 404

@app.errorhandler(500)
def server_error(e):
    return "<h1>500 - Server error</h1>", 500

if __name__ == "__main__":
    app.run(debug=True)
