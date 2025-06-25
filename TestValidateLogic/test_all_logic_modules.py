import os
import sys

# ✅ Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# ✅ Import from project modules
from prototype.load_logic import load_language_logic_map

# Dummy validator — replace with your real one if needed
def validate_logic(logic_entries):
    for entry in logic_entries:
        assert "patterns" in entry and isinstance(entry["patterns"], list), "Missing or invalid 'patterns'"
        assert "response" in entry and isinstance(entry["response"], str), "Missing or invalid 'response'"
        assert "tags" in entry and isinstance(entry["tags"], list), "Missing or invalid 'tags'"

def test_all_logic_modules():
    logic_map = load_language_logic_map()
    total_checked = 0
    total_errors = 0

    for language, parks in logic_map.items():
        for park, regions in parks.items():
            for region, logic_entries in regions.items():
                try:
                    validate_logic(logic_entries)
                    print(f"✅ {language}/{park}/{region} passed validation.")
                    total_checked += 1
                except Exception as e:
                    print(f"❌ {language}/{park}/{region} failed: {e}")
                    total_errors += 1

    print(f"\n🧪 Validation complete: {total_checked} logic modules checked.")
    if total_errors > 0:
        print(f"❗ {total_errors} module(s) failed validation.")
    else:
        print("🎉 All logic modules passed.")

if __name__ == "__main__":
    test_all_logic_modules()
