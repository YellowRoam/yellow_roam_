import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from cors_config import configure_cors
from dotenv import load_dotenv
import openai
import stripe
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from flask_cors import CORS

# === Load Environment Variables ===
load_dotenv()
print("✅ Environment loaded")
print("✅ OPENAI Key:", os.getenv("OPENAI_API_KEY"))
print("✅ STRIPE Key:", os.getenv("STRIPE_SECRET_KEY"))
# === Flask App Setup ===
app = Flask(__name__, static_folder="static", template_folder="templates")
configure_cors(app)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# === Logging Setup ===
logging.basicConfig(filename='yellowroam.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# === Session Store for Free Tier (temporary storage, resets on restart) ===
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
    return f"Use the data below to assist the user.\n\n{context}\n\nUser Question: {user_input}\n\nYour Answer:"

# === Routes ===
@app.route("/")
def home():
    return render_template("OriginalLayout.html")

@app.route("/api/logic/<region>", methods=["GET"])
def get_region_logic(region):
    logic_path = f"./logic/{region}_logic.json"
    if os.path.exists(logic_path):
        with open(logic_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Region not found"}), 404

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        logic_data = data.get('logic', {})

        system_prompt = f"""
        You are YellowRoam, a travel planning expert for the Yellowstone region. Answer user questions with accurate, personalized travel logic.

        Include this context:
        {json.dumps(logic_data, indent=2)}
        """

        ai_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        response_text = ai_response['choices'][0]['message']['content']
        response = jsonify({"response": response_text})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        response = jsonify({'error': str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500

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
        msg["From"] = os.getenv("SMTP_USER")
        msg["Reply-To"] = email

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

if __name__ == '__main__':
    app.run(debug=True)
