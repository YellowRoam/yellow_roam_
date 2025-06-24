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
from yellowroam_fallback_wrapper import handle_user_prompt
from system_prompt_loader import get_prompt_for_app  # includes user profile internally
import importlib.util

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Flask App Setup ===
app = Flask(__name__)
app.config.from_object(ProductionConfig)

if os.environ.get('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# === Logger Setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("YellowRoam")

# === Load System Prompt (dynamically generated based on user session) ===
logic_base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(logic_base, "fallbacks", "yellowstone_system_prompt.json"), "r", encoding="utf-8") as f:
system_prompt = get_prompt_for_app()
print(system_prompt["description"])


def load_py_logic_modules(root_dir):
    logic_map = {}
    for root, _, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(".py"):
                module_path = os.path.join(root, filename)
                module_name = os.path.splitext(filename)[0]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    logic_map[module_name] = getattr(module, "logic_data", [])
                    logger.info(f"📁 Loaded logic from {module_name} ({len(logic_map[module_name])} entries)")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load {module_path}: {e}")
    return logic_map

logic_folder = os.path.join(logic_base, "prototype", "logic")
language_logics = load_py_logic_modules(logic_folder)


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
    data = request.get_json()
    prompt = data.get("prompt") or data.get("message")
    language = data.get("language") or data.get("lang", "en")
    tier = data.get("tier", "free")

    logger.info("💬 /api/chat route hit")
    logger.info(f"📨 Prompt: {prompt}")
    logger.info(f"🌍 Language: {language} | 🎟️ Tier: {tier}")

    if not prompt:
        logger.warning("⚠️ No prompt received.")
        return jsonify({"error": "No prompt received."}), 400

    local_logic = language_logics.get(language, language_logics.get("en", []))
    local_response = match_local_logic(prompt, language, tier, local_logic)
    if local_response:
        logger.info("✅ Local logic match returned.")
        return jsonify({"response": local_response})

    smart_response = smart_match_logic(prompt, language, tier, language_logics)
    if smart_response:
        logger.info("🧠 Smart logic match returned from expanded intent/tags.")
        return jsonify({"response": smart_response})

    log_unmatched_prompt(prompt, language, tier)
    logger.warning("❌ No match found in local or smart logic. Logged for future coverage.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt["description"] + " " + system_prompt["role"]},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"response": response.choices[0].message["content"]})
    except Exception as e:
        logger.error(f"🔥 OpenAI fallback failed: {e}")
        fallback_msg = {
            "en": "Sorry, I don’t know the answer to that yet!",
            "es": "Lo siento, ¡aún no sé la respuesta a eso!",
            "fr": "Désolé, je ne connais pas encore la réponse à cela !",
            "hi": "माफ़ कीजिए, मुझे इसका उत्तर अभी नहीं पता!"
        }
        return jsonify({"response": fallback_msg.get(language, fallback_msg["en"])})

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
    app.run(debug=True)
