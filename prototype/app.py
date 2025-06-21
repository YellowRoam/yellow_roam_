import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import openai

# === Load environment variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Flask App Setup ===
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}})

# === Logger Setup ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YellowRoam")

# === Load Logic Files ===
logic_folder = os.path.join(os.path.dirname(__file__), "logic")
language_logics = {}
logic_filenames = [f for f in os.listdir(logic_folder) if f.endswith(".json")]

def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"⚠️ Failed to load {path}: {e}")
        return {}

for filename in logic_filenames:
    filepath = os.path.join(logic_folder, filename)
    lang_code = filename.split(".")[0]
    language_logics[lang_code] = load_json_file(filepath)

# === Match Local Logic ===
def match_local_logic(prompt, language, tier):
    logic_sets = [language_logics.get(language, {}), language_logics.get("intent", {})]
    for logic_set in logic_sets:
        if isinstance(logic_set, list):
            for entry in logic_set:
                if "patterns" in entry and any(p.lower() in prompt.lower() for p in entry["patterns"]):
                    if "tiers" not in entry or tier in entry["tiers"]:
                        entry["source"] = logic_set
                        return entry["response"]
    return None

import re

def smart_match_logic(prompt, language, tier, logic_files):
    prompt_lower = prompt.lower().strip()

    # === Normalize & Define intent/topic triggers ===
    intent_triggers = {
        "lodging": ["hotel", "place to stay", "stay", "lodging", "accommodation", "motel", "airbnb"],
        "food": ["eat", "food", "restaurant", "breakfast", "dinner", "pizza", "coffee"],
        "activity": ["things to do", "activities", "fun", "hiking", "swimming", "biking", "fishing", "skiing"],
        "wildlife": ["see bison", "bears", "wolves", "wildlife watching", "animal"],
        "trails": ["hike", "trail", "easy walk", "moderate hike", "strenuous hike"],
        "hot springs": ["hot spring", "soak", "natural spring"],
        "camping": ["campground", "tent site", "rv park", "camp", "campsite"]
    }

    tag_keywords = ["kid-friendly", "pet-friendly", "budget", "luxury", "open year-round", "summer", "winter"]

    matched_intent = None
    for intent, triggers in intent_triggers.items():
        if any(trigger in prompt_lower for trigger in triggers):
            matched_intent = intent
            break

    matched_tags = [tag for tag in tag_keywords if tag in prompt_lower]

    # === Town/region extraction ===
    town_files = {
        "bozeman": "bozeman.logic.json",
        "jackson": "jackson_driggs.logic.json",
        "driggs": "jackson_driggs.logic.json",
        "gardiner": "livingston_gardiner.logic.json",
        "cody": "cody_cook_city.logic.json",
        "west yellowstone": "bozeman.logic.json",
        "grand teton": "grand_teton.logic.json",
        "big sky": "big_sky.logic.json",
        "ennis": "ennis_virginia_city.logic.json",
        "virginia city": "ennis_virginia_city.logic.json"
    }

    selected_logic_files = []

    for town, filename in town_files.items():
        if town in prompt_lower:
            selected_logic_files.append(filename)

    if not selected_logic_files:
        selected_logic_files = list(logic_files.keys())  # scan all files if no town matched

    # === Match patterns across files ===
    for logic_file in selected_logic_files:
        logic_data = logic_files.get(logic_file.replace(".logic.json", ""), [])
        for entry in logic_data:
            if "patterns" in entry:
                for pattern in entry["patterns"]:
                    if re.search(rf"\b{re.escape(pattern.lower())}\b", prompt_lower):
                        if "tiers" not in entry or tier in entry["tiers"]:
                            if matched_tags:
                                if "tags" in entry and all(tag in entry["tags"] for tag in matched_tags):
                                    return entry["response"]
                            else:
                                return entry["response"]

    return None  # fallback triggers OpenAI

# === Log unmatched prompts ===
def log_unmatched_prompt(prompt, language, tier):
    try:
        log_entry = {"prompt": prompt, "language": language, "tier": tier}
        with open("unmatched_prompts.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        logger.error(f"Logging failed: {e}")

# === Routes ===
@app.route("/")
def index():
    return render_template("index.html")

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

    # Step 1: Try local logic
    local_response = match_local_logic(prompt, language, tier)
    if local_response:
        logger.info("✅ Local logic match returned.")
        return jsonify({"response": local_response})

    # Step 2: Try smart match (pattern+tag+location based)
    smart_response = smart_match_logic(prompt, language, tier, language_logics)
    if smart_response:
        logger.info("🧠 Smart logic match returned from expanded intent/tags.")
        return jsonify({"response": smart_response})

    # Step 3: Log and fallback to OpenAI or default message
    log_unmatched_prompt(prompt, language, tier)
    logger.warning("❌ No match found in local or smart logic. Logged for future coverage.")

    try:
        system_prompt = language_logics.get(language, language_logics.get("en", {}))
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": json.dumps(system_prompt)},
                {"role": "user", "content": prompt}
            ]
        )
        logger.info("🔁 OpenAI fallback successful.")
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

    
    # === Route: Yellowstone Props (placeholder) ===
@app.route("/api/yellowstone_props", methods=["GET"])
def yellowstone_props():
    # In future, you can dynamically generate this
    return jsonify({
        "description": "Yellowstone National Park logic API",
        "modules": list(language_logics.keys()),
        "routes": ["/", "/yellowroamprompts", "/api/chat", "/api/yellowstone_props"]
    })

# === 404 Error Handler ===
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Route not found", "status": 404}), 404

# === Run the app ===
if __name__ == "__main__":
    print("✅ YellowRoam is running at http://localhost:5000")
    app.run(debug=True)
