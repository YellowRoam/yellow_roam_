
import re
import logging

logger = logging.getLogger("YellowRoam")

def smart_match_logic(prompt, language, tier, logic_files):
    prompt_lower = prompt.lower().strip()
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

    matched_tags = [tag for tag in tag_keywords if tag in prompt_lower]

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

    selected_logic_files = [filename for town, filename in town_files.items() if town in prompt_lower]
    if not selected_logic_files:
        selected_logic_files = list(logic_files.keys())

    for logic_file in selected_logic_files:
        logic_data = logic_files.get(logic_file.replace(".logic.json", ""), [])
        if not isinstance(logic_data, list):
            logger.warning(f"⚠️ Logic file '{logic_file}' is not a list.")
            continue

        for entry in logic_data:
            if "patterns" in entry:
                for pattern in entry["patterns"]:
                    try:
                        pattern_lower = pattern.lower().strip()
                        if re.search(rf"\b{re.escape(pattern_lower)}\b", prompt_lower):
                            if "tiers" not in entry or tier in entry["tiers"]:
                                if matched_tags:
                                    if "tags" in entry and all(tag in entry["tags"] for tag in matched_tags):
                                        logger.info(f"✅ Smart match with tags in '{logic_file}' using pattern '{pattern}'.")
                                        return entry["response"]
                                else:
                                    logger.info(f"✅ Smart match in '{logic_file}' using pattern '{pattern}'.")
                                    return entry["response"]
                    except Exception as e:
                        logger.error(f"Regex match failed for pattern '{pattern}' in smart_match_logic: {e}")
    logger.debug("❌ No smart pattern matched.")
    return None
