import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from openai import OpenAI  # ✅ Correct import for v1.3.9

# === Load environment variables ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")

# === Initialize OpenAI client ===
client = OpenAI(api_key=OPENAI_API_KEY)

# === Flask app setup ===
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# === Logging setup ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("yellowroam")

# === Health check route ===
@app.route("/")
def home():
    return "✅ YellowRoam backend is running."

# === Chat route ===
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "Missing 'message' field in JSON request"}), 400

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Yellowstone travel assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})

    except Exception as e:
        logger.error(f"🔥 Error in /api/chat: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# === Run app (if needed locally) ===
if __name__ == "__main__":
    app.run(debug=True)
