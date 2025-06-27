import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import openai 

from prototype.config import DevelopmentConfig, ProductionConfig
from prototype.match_local_logic import match_local_logic
from prototype.smart_match_logic import smart_match_logic
from prototype.fallback_router import route_fallback
from prototype.fallback_wrapper import handle_user_prompt
from prototype.load_logic import load_language_logic_map
from prototype.response_handler import respond


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai


Flask App Setup 
app = Flask(__name__)
if os.environ.get('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

CORS(app, resources={r"/api/*": {"origins": "*"}})


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("YellowRoam")

 Base Logic Folder
logic_base = os.path.dirname(os.path.abspath(__file__))

Load Logic Modules
language_logics = load_language_logic_map()

Prompt Logging
def log_unmatched_prompt(prompt, language, tier):
    try:
        log_entry = {"prompt": prompt, "language": language, "tier": tier}
        with open("unmatched_prompts.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        logger.error(f"Logging failed: {e}")


@app.route("/yellowroamprompts")
def yellowroam_prompt():
    return render_template("yellowroamprompts.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    print("/api/chat route was hit")
    try:
        data = request.get_json()
        print("Payload received:", data)

        return jsonify({"response": "Test response from /api/chat"})
    except Exception as e:
        print(f"Error in /api/chat: {e}")
        return jsonify({"error": "Internal error"}), 500


        }
    })

@app.route("/fallback", methods=["POST"])
def fallback():
    data = request.get_json()
    prompt = data.get("prompt", "")
    user_id = data.get("user_id", "anonymous")
    location = data.get("location", "Yellowstone")

    match = route_fallback(prompt)
    if match:
        return jsonify({"response": match["response"], "source": "logic_match"})

    handled = handle_user_prompt(prompt, user_id=user_id, location=location)
    return jsonify({
        "response": handled["response"],
        "source": "tone_wrapper",
        "log": handled["log"],
        "timestamp": handled["timestamp"]
    })

@app.route("/api/yellowstone_props", methods=["GET"])
def yellowstone_props():
    return jsonify({
        "description": "Yellowstone National Park logic API",
        "modules": list(language_logics.keys()),
        "routes": ["/", "/yellowroamprompts", "/api/chat", "/api/yellowstone_props"]
    })

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Route not found", "status": 404}), 404

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    result = route_fallback("Where can I fish in Yellowstone?")
    if result:
        print(result["response"])
