# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import traceback

#Import YellowRoam response logic 
from prototype.response_handler import respond

#Logging Setup 
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger("YellowRoam")

#lask App Setup 
app = Flask(__name__)
CORS(app)

#Health Check Route
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "YellowRoam backend is active",
        "version": "1.0.0",
        "message": "Send a POST request to /ask with a prompt and metadata."
    }), 200

#Main Inference Route 
@app.route("/ask", methods=["POST"])
def handle_ask():
    try:
        # Accept both JSON and form-data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Required
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "Missing required field: 'prompt'"}), 400

        # Optional (with default fallbacks)
        user_id = data.get("user_id", "anonymous")
        location = data.get("location", "unknown")
        tier = data.get("tier", "free")
        language = data.get("language", "en")
        region = data.get("region", "yellowstone")  # Default scope is Yellowstone

        logger.info(
            f"[Prompt Received] '{prompt}' | user_id={user_id}, location={location}, tier={tier}, lang={language}, region={region}"
        )

        # Call YellowRoam’s main logic handler
        response_text = respond(
            prompt=prompt,
            user_id=user_id,
            location=location,
            tier=tier,
            language=language,
            region=region,
        )

        logger.info(f"[Response Sent] user_id={user_id}")
        return jsonify({"response": response_text}), 200

    except Exception as e:
        logger.error("Unhandled exception during prompt processing")
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

#App Runner
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    debug_mode = os.environ.get("DEBUG", "false").lower() == "true"
    logger.info(f"Starting YellowRoam Flask app on port {port} (debug={debug_mode})")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
