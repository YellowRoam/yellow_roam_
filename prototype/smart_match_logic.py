import re
import logging
from prototype.Logic_Data import LogicDataTierFree  # ✅ unified logic set

logger = logging.getLogger("YellowRoam")

# Unified logic map using cleaned, tier-aligned module
logic_map = {
    "unified": LogicDataTierFree.logic
}

def smart_match_logic(prompt, language, tier, logic_files=logic_map):
    prompt_lower = prompt.lower().strip()

    # Intent classification
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

    for logic_name, logic_data in logic_files.items():
        if not isinstance(logic_data, list):
            logger.warning(f"⚠️ Logic for '{logic_name}' is not a list.")
            continue

        for entry in logic_data:
            if "patterns" not in entry:
                continue

            for pattern in entry["patterns"]:
                try:
                    pattern_lower = pattern.lower().strip()
                    if re.search(rf"\b{re.escape(pattern_lower)}\b", prompt_lower):
                        if "tier" not in entry or entry["tier"] == tier:
                            if matched_tags:
                                if "tags" in entry and all(tag in entry["tags"] for tag in matched_tags):
                                    logger.info(f"✅ Smart match (with tags) in '{logic_name}' using pattern '{pattern}'")
                                    return entry["response"]
                            else:
                                logger.info(f"✅ Smart match in '{logic_name}' using pattern '{pattern}'")
                                return entry["response"]
                except Exception as e:
                    logger.error(f"❌ Regex failed in smart_match_logic for pattern '{pattern}': {e}")

    logger.debug("❌ No smart pattern matched.")
    return None
