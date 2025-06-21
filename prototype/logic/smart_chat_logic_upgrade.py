
import logging
from rapidfuzz import fuzz

logger = logging.getLogger("YellowRoam")

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

def expand_with_synonyms(prompt):
    prompt_words = prompt.lower().split()
    expanded_prompt = set(prompt_words)
    for word in prompt_words:
        if word in SYNONYMS:
            expanded_prompt.update(SYNONYMS[word])
    return " ".join(expanded_prompt)

def smart_match_logic(prompt, language, tier, logic_files):
    prompt_lower = prompt.lower().strip()
    expanded_prompt = expand_with_synonyms(prompt_lower)

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
            selected_logic_files.append(filename.replace(".logic.json", ""))

    if not selected_logic_files:
        selected_logic_files = list(logic_files.keys())

    logger.info(f"🔍 Expanded prompt: '{expanded_prompt}' scanning: {selected_logic_files}")

    for logic_key in selected_logic_files:
        logic_data = logic_files.get(logic_key, [])
        for entry in logic_data:
            if "patterns" in entry:
                for pattern in entry["patterns"]:
                    # Use fuzzy match threshold and expanded prompt
                    fuzz_score = fuzz.partial_ratio(pattern.lower(), expanded_prompt)
                    if fuzz_score >= 75:
                        if "tiers" not in entry or tier in entry["tiers"]:
                            if "tags" in entry:
                                if all(tag in expanded_prompt for tag in entry["tags"]):
                                    logger.info(f"✅ Fuzzy + Tag match: {pattern} with score {fuzz_score}")
                                    return entry["response"]
                            else:
                                logger.info(f"✅ Fuzzy match: {pattern} with score {fuzz_score}")
                                return entry["response"]

    logger.info(f"❌ No match after fuzzy + synonym scan.")
    return None
