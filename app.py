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
from prototype.yellowstone_system_prompt import system_prompt



app = Flask(__name__)


#Environment and API Setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai

if os.environ.get('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

CORS(app, resources={r"/api/*": {"origins": "*"}})

#Logger Setup 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
        
        except Exception as e:
        logger.error(f" OpenAI fallback failed: {e}")
        fallback_msg = "Sorry, I don’t know the answer to that yet!"
        return jsonify({"response": fallback_msg})

logger = logging.getLogger("YellowRoam")

# Base Logic Folder
logic_base = os.path.dirname(os.path.abspath(__file__))

# Load Logic Modules
language_logics = load_language_logic_map()

#Prompt Logging 

def log_unmatched_prompt(prompt, language, tier):
    try:
        log_entry = {"prompt": prompt, "language": language, "tier": tier}
        with open("unmatched_prompts.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    

@app.route("/yellowroamprompts")
def yellowroam_prompt():
    return render_template("yellowroamprompts.html")

@app.route("/chat", methods=["POST"])



@app.route("/api/chat", methods=["POST"])
def chat():
    prompt = request.json.get("message", "")
    language = request.json.get("language", "en")
    tier = request.json.get("tier", "free")

    logger.info("/api/chat route hit")
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Language: {language} | Tier: {tier}")

    if not prompt:
        logger.warning("No prompt received.")
        return jsonify({"error": "No prompt received."}), 400

    local_logic = language_logics.get(language, language_logics.get("en", []))
    local_response = match_local_logic(prompt, language, tier, local_logic)
    if local_response:
        logger.info("Local logic match returned.")
        return jsonify({"response": local_response})

    smart_response = smart_match_logic(prompt, language, tier, language_logics)
    if smart_response:
        logger.info("Smart logic match returned from expanded intent/tags.")
        return jsonify({"response": smart_response})

    log_unmatched_prompt(prompt, language, tier)
    logger.warning("No match found in local or smart logic. Logged for future coverage.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt["description"] + " " + system_prompt.get("role", "")},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"response": response.choices[0].message["content"]})
    except Exception as e:
        logger.error(f" OpenAI fallback failed: {e}")
        fallback_msg = "Sorry, I don’t know the answer to that yet!"
        return jsonify({"response": fallback_msg})

            , \u092e\u0941\u091d\u0947 \u0907\u0938\u0915\u093e \u0909\u0924\u094d\u0924\u0930 \u0905\u092d\u0940 \u0928\u0939\u0940\u0902 \u092a\u0924\u093e!"
        }
        return jsonify({"response": fallback_msg.get(language, fallback_msg["en"])})

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
    return render_template("404.html"), 404

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    result = route_fallback("Where can I fish in Yellowstone?")
    if result:
        print(result["response"])


    
