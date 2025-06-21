
import json
from flask import Flask, request, jsonify
from difflib import SequenceMatcher
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YellowRoamUnifiedRouter")

# === Synonym Map ===
SYNONYMS = {
    "brewery": ["breweries", "beer", "taproom", "alehouse"],
    "hike": ["trail", "walk", "trek", "path"],
    "food": ["restaurant", "dining", "eatery", "cuisine", "meal"],
    "lodging": ["hotel", "accommodation", "motel", "place to stay", "room"],
    "camping": ["tent", "campground", "rv park", "campsite"],
    "wildlife": ["animals", "bison", "bear", "wolves", "elk"],
    "hot springs": ["soak", "thermal", "natural spring"],
    "ski": ["snow", "snowboarding", "powder", "resort"]
}

def expand_with_synonyms(text):
    words = text.lower().split()
    expanded = set(words)
    for word in words:
        if word in SYNONYMS:
            expanded.update(SYNONYMS[word])
    return " ".join(expanded)

def fuzzy_score(a, b):
    return SequenceMatcher(None, a, b).ratio()

# === Load Logic Data ===
with open('YellowRoam_Logic_Full.json', 'r') as f:
    logic_data = json.load(f)

with open('chat_logic_config.json', 'r') as f:
    config = json.load(f)

with open('YellowRoam_Fallbacks_Logic.json', 'r') as f:
    fallback_data = json.load(f)

# === Keyword Map ===
keyword_map = config.get('keywords', {})

def extract_keywords(text):
    hits = set()
    for tag, words in keyword_map.items():
        if any(word in text for word in words):
            hits.add(tag)
    return hits

def match_query(query, region=None, tier=None, threshold=0.65):
    expanded_query = expand_with_synonyms(query)
    keyword_hits = extract_keywords(expanded_query)
    best_match = None
    best_score = 0

    logger.info(f"🔍 Expanded query: '{expanded_query}'")

    for item in logic_data:
        score = 0

        # Tier check
        if tier and tier not in item.get("tiers", ["free"]):
            continue

        # Region check
        if region and region.lower() in item.get("tags", []):
            score += 3

        # Fuzzy match on patterns
        for pattern in item.get("patterns", []):
            fuzz_val = fuzzy_score(pattern.lower(), expanded_query)
            if fuzz_val >= threshold:
                score += int(fuzz_val * 10)
                logger.debug(f"Pattern: '{pattern}' => score: {fuzz_val:.2f}")

        # Keyword match boost
        for tag in item.get("tags", []):
            if tag in keyword_hits:
                score += 2

        if score > best_score:
            best_score = score
            best_match = item

    if best_match:
        logger.info(f"✅ Match found: Score={best_score}, Response='{best_match['response'][:60]}...'")
        return best_match
    else:
        logger.warning("❌ No strong match found in primary logic.")
        return None

def match_fallback(query):
    query_lower = query.lower()
    for fallback in fallback_data:
        if any(word in query_lower for word in fallback.get("keywords", [])):
            logger.info(f"🪂 Fallback matched for keyword: '{fallback['keywords']}'")
            return {"response": fallback.get("response", "Fallback response not found.")}
    logger.info("🪂 Default fallback used.")
    return {"response": "Sorry, we couldn’t find a perfect answer, but here’s something helpful: Explore local visitor centers or our seasonal tips guide."}

@app.route("/query", methods=["POST"])
def handle_query():
    data = request.json
    query = data.get("query", "")
    region = data.get("region")
    tier = data.get("tier")
    match = match_query(query, region, tier)
    if not match:
        match = match_fallback(query)
    return jsonify(match)
