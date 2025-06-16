import traceback
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

openai.api_key = os.getenv("OPENAI_API_KEY") 


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


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        input_text = data.get("message", "")
        location = data.get("location", "unknown")

        print("🟡 Received message:", input_text, "| Location:", location)
        print("✅ Final OpenAI Key in use:", os.getenv("OPENAI_API_KEY"))

        openai.api_key = os.getenv("OPENAI_API_KEY")
        print("⏳ Sending request to OpenAI")

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))        
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input_text}],
            max_tokens=100
        )

        reply = response['choices'][0]['message']['content']
        print("🟢 AI response:", reply)

        return jsonify({"response": reply})

    except Exception as e:
        print("🔴 EXCEPTION TRIGGERED IN /api/chat")
        print(f"🔴 Error message: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "error": "Something went wrong",
            "details": str(e)
        }), 500



       
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
