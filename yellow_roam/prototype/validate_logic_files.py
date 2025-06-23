
import os
import json

LOGIC_FOLDER = os.path.join(os.path.dirname(__file__), "prototype", "logic")

def validate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"❌ ERROR in {filepath}: Top-level JSON must be a list.")
                return False
            for entry in data:
                if "patterns" not in entry or not isinstance(entry["patterns"], list):
                    print(f"❌ ERROR in {filepath}: Missing or invalid 'patterns' in entry.")
                    return False
                if "response" not in entry:
                    print(f"❌ ERROR in {filepath}: Missing 'response' in entry.")
                    return False
            print(f"✅ VALID: {os.path.basename(filepath)}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ JSON Error in {filepath}: {e}")
            return False

def main():
    all_files = [f for f in os.listdir(LOGIC_FOLDER) if f.endswith(".json")]
    print(f"🔍 Scanning {len(all_files)} logic files...\n")
    for filename in all_files:
        filepath = os.path.join(LOGIC_FOLDER, filename)
        validate_file(filepath)

if __name__ == "__main__":
    main()
