
# match_local_logic.py

import re
import logging
from prototype.validate_logic_files import validate_logic
from prototype.response_handler import respond

from Yellowstone_Fallbacks.flower_logic import entries as flower_entries
from Yellowstone_Fallbacks.hiking_logic import entries as hiking_entries
from Yellowstone_Fallbacks.camping_logic import entries as camping_entries
from Yellowstone_Fallbacks.fishing_logic import entries as fishing_entries
from Yellowstone_Fallbacks.fishing_logic_v2 import entries as fishing_v2_entries
from Yellowstone_Fallbacks.fishing_logic_v3 import entries as fishing_v3_entries
from Yellowstone_Fallbacks.photography_logic import entries as photography_entries
from Yellowstone_Fallbacks.mammoth_logic import entries as mammoth_entries
from Yellowstone_Fallbacks.weather_logic import entries as weather_entries
from Yellowstone_Fallbacks.directions_logic import entries as directions_entries
from Yellowstone_Fallbacks.directions_logic_v2 import entries as directions_v2_entries
from Yellowstone_Fallbacks.directions_logic_v3 import entries as directions_v3_entries
from Yellowstone_Fallbacks.winter_recreation_logic import entries as winter_entries
from Yellowstone_Fallbacks.norris_logic_v2 import entries as norris_entries


# Combine all entries into one flat list
all_entries = (
    flower_entries +
    hiking_entries +
    camping_entries +
    fishing_entries +
    fishing_v2_entries +
    fishing_v3_entries +
    photography_entries +
    mammoth_entries +
    weather_entries +
    directions_entries +
    directions_v2_entries +
    directions_v3_entries +
    winter_entries +
    norris_entries
)


def match_fallback(user_input: str, entries: list):
    # simple matching fallback function
    for entry in entries:
        patterns = entry.get("patterns", [])
        for pattern in patterns:
            if pattern.lower() in user_input.lower():
                return entry.get("response", " I found a match, but there's no response defined.")
    return None


def match_local_logic(prompt, language, tier, logic_data):
    prompt = prompt.lower().strip()

    if not isinstance(logic_data, list):
        logger.warning(f" Logic data for language '{language}' is not a list.")
        return None

    for entry in logic_data:
        patterns = entry.get("patterns", [])
        tiers = entry.get("tiers", ["free"])
        lang = entry.get("language", "en")

        if language != lang or tier not in tiers:
            continue

        for pattern in patterns:
            if re.search(pattern, prompt):
                logger.info(f" Matched pattern: {pattern}")
                return respond(entry)

    logger.info(" No matching logic entry found.")
    return None

