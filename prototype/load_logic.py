import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Yellowstone_Fallbacks import (
    camping_logic,
    directions_logic,
    directions_logic_v2,
    directions_logic_v3,
    fishing_logic,
    fishing_logic_v2,
    flower_logic,
    hiking_logic,
    mammoth_logic,
    norris_logic_v2,
    photography_logic,
    weather_logic,
    winter_recreation_logic
)

def load_language_logic_map():
    return {
        "en": {
            "yellowstone": {
                "campground": camping_logic.entries,
                "directions": directions_logic.entries,
                "directions_v2": directions_logic_v2.entries,
                "directions_v3": directions_logic_v3.entries,
                "fishing": fishing_logic.entries,
                "fishing_v2": fishing_logic_v2.entries,
                "flower": flower_logic.entries,
                "hiking": hiking_logic.entries,
                "mammoth": mammoth_logic.entries,
                "norris_v2": norris_logic_v2.entries,
                "photography": photography_logic.entries,
                "weather": weather_logic.entries,
                "winter_recreation": winter_recreation_logic.entries
            }
        }
    }
