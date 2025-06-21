
import re
import logging

logger = logging.getLogger("YellowRoam")

def match_local_logic(prompt, language, tier, logic_data):
    prompt = prompt.lower().strip()
    if not isinstance(logic_data, list):
        logger.warning(f"⚠️ Logic data for language '{language}' is not a list.")
        return None

    for entry in logic_data:
        if "patterns" in entry:
            for pattern in entry["patterns"]:
                try:
                    pattern_lower = pattern.lower().strip()
                    if re.search(rf"\b{re.escape(pattern_lower)}\b", prompt):
                        if "tiers" not in entry or tier in entry["tiers"]:
                            logger.info(f"✅ Pattern matched: '{pattern}' in local logic.")
                            return entry["response"]
                except Exception as e:
                    logger.error(f"Regex match failed for pattern '{pattern}': {e}")
    logger.debug("❌ No pattern matched in match_local_logic.")
    return None
