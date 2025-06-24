import re
import logging
from prototype.validate_logic_files import validate_logic
from prototype.response_handler import respond

logger = logging.getLogger("YellowRoam")

def match_local_logic(prompt, language, tier, logic_data):
    prompt = prompt.lower().strip()

    if not isinstance(logic_data, list):
        logger.warning(f"⚠️ Logic data for language '{language}' is not a list.")
        return None

    for entry in logic_data:
        patterns = entry.get("patterns", [])
        tiers = entry.get("tiers", ["free"])
        lang = entry.get("language", "en")

        if language != lang or tier not in tiers:
            continue

        for pattern in patterns:
            if re.search(pattern, prompt):
                logger.info(f"✅ Matched pattern: {pattern}")
                return respond(entry)

    logger.info("❌ No matching logic entry found.")
    return None
