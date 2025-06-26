import os
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Import logic map and validator
from prototype.load_logic import load_language_logic_map
from prototype.validate_logic_files import validate_logic

def test_yellowstone_logic_bundle():
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

    print(f"\n🧪 Final validation complete: {total_checked} logic modules checked.")
    if total_errors > 0:
        print(f"❗ {total_errors} module(s) failed validation.")
    else:
        print("🎉 All Yellowstone logic modules passed.")

if __name__ == "__main__":
    test_yellowstone_logic_bundle()
