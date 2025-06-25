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
                "campground": camping_logic,
                "directions": directions_logic,
                "directions_v2": directions_logic_v2,
                "directions_v3": directions_logic_v3,
                "fishing": fishing_logic,
                "fishing_v2": fishing_logic_v2,
                "flower": flower_logic,
                "hiking": hiking_logic,
                "mammoth": mammoth_logic,
                "norris_v2": norris_logic_v2,
                "photography": photography_logic,
                "weather": weather_logic,
                "winter_recreation": winter_recreation_logic
            }
        }
    }
