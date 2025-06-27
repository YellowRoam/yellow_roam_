from prototype.YellowstoneNationalPark import (
    campground_logic,
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
        "en": fishing_logic_v2
    }


def load_yellowstone_logic():
    all_modules = [
        campground_logic,
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
    ]

    entries = []
    for module in all_modules:
        name = getattr(module, "__name__", str(module))
        if hasattr(module, "entries") and isinstance(module.entries, list):
            print(f"[✅] Loaded entries from {name}: {len(module.entries)}")
            entries.extend(module.entries)
        else:
            print(f"[❌] Skipping module {name} — no 'entries' list")

    return entries
