
import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS
import openai
import stripe

# === Load Environment Variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# === Flask Setup ===
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}})

# === Logging Setup ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YellowRoam")

# === Helper: Load Logic Files ===
def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"⚠️ Skipping missing file: {path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON decode error in {path}: {e}")
        return {}

# === Load Logic Files ===
logic_folder = os.path.join(os.path.dirname(__file__), "logic")
language_logics = {}
logic_filenames = [
    "intent.logic.json",
    "fallback.logic.json",
    "en.logic.json",
    "es.logic.json",
    "fr.logic.json",
    "hi.logic.json",
    "big_sky.logic.json",
    "bozeman.logic.json",
    "cody_cook_city.logic.json",
    "ennis_virginia_city.logic.json",
    "grand_teton.logic.json",
    "jackson_driggs.logic.json",
    "livingston_gardiner.logic.json",
    "red_lodge_beartooth.logic.json",
    "ski_logic.logic.json"
]

for filename in logic_filenames:
    path = os.path.join(logic_folder, filename)
    lang_code = filename.split(".")[0]
    language_logics[lang_code] = load_json_file(path)

# === Local Logic Processor ===
def match_local_logic(prompt, language, tier):
    logic_sets = [language_logics.get(language, {}), language_logics.get("intent", {})]
    for logic_set in logic_sets:
        if isinstance(logic_set, list):
            for entry in logic_set:
                if "patterns" in entry and any(p.lower() in prompt.lower() for p in entry["patterns"]):
                    if "tiers" not in entry or tier in entry["tiers"]:
                        return entry["response"]
    return None

# === Log unmatched prompts for future coverage ===
def log_unmatched_prompt(prompt, language, tier):
    log_entry = {
        "prompt": prompt,
        "language": language,
        "tier": tier
    }
    try:
        with open("unmatched_prompts.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        logger.error(f"Failed to log unmatched prompt: {e}")

# === Routes ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt") or data.get("message")
    language = data.get("language") or data.get("lang", "en")
    tier = data.get("tier", "free")

    if not prompt:
        return jsonify({"error": "No prompt received."}), 400

    # Step 1: Try local logic
    local_response = match_local_logic(prompt, language, tier)
    if local_response:
        return jsonify({"response": local_response})

    # Step 2: Log and fallback to OpenAI if needed
    log_unmatched_prompt(prompt, language, tier)

    try:
        system_prompt = language_logics.get(language, language_logics.get("en", {}))
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": json.dumps(system_prompt)},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"response": response.choices[0].message["content"]})
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        fallback_msg = {
            "en": "Sorry, I don’t know the answer to that yet!",
            "es": "Lo siento, ¡aún no sé la respuesta a eso!",
            "fr": "Désolé, je ne connais pas encore la réponse à cela !",
            "hi": "माफ़ कीजिए, मुझे इसका उत्तर अभी नहीं पता!"
        }
        return jsonify({"response": fallback_msg.get(language, fallback_msg["en"])})

if __name__ == "__main__":
    app.run(debug=True)
