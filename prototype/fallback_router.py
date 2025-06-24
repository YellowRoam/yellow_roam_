import json
import logging
from pathlib import Path
from rapidfuzz import fuzz
from prototype.match_local_logic import match_local_logic

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Load all fallback entries ===
def load_all_fallback_entries(directory: str):
    entries = []
    fallback_files = Path(directory).glob("*.json")
    for file in fallback_files:
        try:
            with open(file, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    entries.extend(data)
                    logger.info(f"✅ Loaded {len(data)} entries from {file.name}")
                else:
                    logger.warning(f"⚠️ Skipping {file.name}: not a list")
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON in file: {file.name}")
    logger.info(f"🧠 Total fallback entries loaded: {len(entries)}")
    return entries

# === Match logic ===
def match_fallback(user_input: str, entries: list, threshold: int = 75):
    best_match = None
    highest_score = 0
    for entry in entries:
        for pattern in entry.get("patterns", []):
            score = fuzz.token_sort_ratio(user_input.lower(), pattern.lower())
            if score > highest_score and score >= threshold:
                highest_score = score
                best_match = entry
    logger.info(f"🔍 Best match score: {highest_score}")
    return best_match

# === MAIN FUNCTION — PASTE THIS BLOCK ===
def main():
    # You call it HERE
    entries = load_all_fallback_entries("./fallbacks")

    # Now the entries list is ready for matching
    user_input = input("🔎 Ask something about Yellowstone: ")
    match = match_fallback(user_input, entries)

    if match:
        print("🟢 Matched response:\n", match["response"])
    else:
        print("❌ No match found.")

# === RUN SCRIPT ===
if __name__ == "__main__":
    main()

