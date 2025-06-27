# validate_logic_files.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def validate_logic(logic_entries):
    """
    Validates a list of fallback logic entries.
    Returns True if all entries pass validation, else raises ValueError.
    """
    if not isinstance(logic_entries, list):
        raise ValueError("Logic must be a list of entries.")

    for i, entry in enumerate(logic_entries):
        if not isinstance(entry, dict):
            raise ValueError(f"Entry {i} is not a dict.")

        # Required fields
        for field in ["patterns", "response", "tier"]:
            if field not in entry:
                raise ValueError(f"Entry {i} missing required field: '{field}'")

        # Validate patterns
        patterns = entry["patterns"]
        if not isinstance(patterns, list) or not patterns:
            raise ValueError(f"Entry {i}: 'patterns' must be a non-empty list.")
        if not all(isinstance(p, str) for p in patterns):
            raise ValueError(f"Entry {i}: all 'patterns' must be strings.")

        # Validate response
        if not isinstance(entry["response"], str):
            raise ValueError(f"Entry {i}: 'response' must be a string.")

        # Optional tags
        if "tags" in entry:
            if not isinstance(entry["tags"], list):
                raise ValueError(f"Entry {i}: 'tags' must be a list.")
            if not all(isinstance(tag, str) for tag in entry["tags"]):
                raise ValueError(f"Entry {i}: all 'tags' must be strings.")

        # Tier check
        if entry["tier"] not in ("free", "pro"):
            raise ValueError(f"Entry {i}: 'tier' must be 'free' or 'pro'.")

    return True


if __name__ == "__main__":
    # Import validated Yellowstone logic modules
    from Yellowstone_Fallbacks import (
        flower_logic,
        hiking_logic,
        camping_logic,
        fishing_logic,
        fishing_logic_v2,
        fishing_logic_v3,
        photography_logic,
        mammoth_logic,
        weather_logic,
        directions_logic,
        directions_logic_v2,
        directions_logic_v3,
        winter_recreation_logic,
        norris_logic_v2
    )

    logic_sets = {
        "flower_logic": flower_logic.entries,
        "hiking_logic": hiking_logic.entries,
        "camping_logic": camping_logic.entries,
        "fishing_logic": fishing_logic.entries,
        "fishing_logic_v2": fishing_logic_v2.entries,
        "fishing_logic_v3": fishing_logic_v3.entries,
        "photography_logic": photography_logic.entries,
        "mammoth_logic": mammoth_logic.entries,
        "weather_logic": weather_logic.entries,
        "directions_logic": directions_logic.entries,
        "directions_logic_v2": directions_logic_v2.entries,
        "directions_logic_v3": directions_logic_v3.entries,
        "winter_recreation_logic": winter_recreation_logic.entries,
        "norris_logic_v2": norris_logic_v2.entries
    }

    failures = 0

    for name, logic in logic_sets.items():
        try:
            validate_logic(logic)
            print(f"{name} passed validation.")
        except Exception as e:
            print(f" {name} failed validation: {e}")
            failures += 1

    if failures:
        print(f"\n{failures} logic set(s) failed validation.")
        exit(1)
    else:
        print("\n All logic sets passed validation.")
