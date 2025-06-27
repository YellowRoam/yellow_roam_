import sys
import re
import os
import importlib.util

def load_fallback_modules(folder_path):
    fallback_entries = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and filename != "__init__.py":
            full_path = os.path.join(folder_path, filename)
            spec = importlib.util.spec_from_file_location(filename, full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Support both fallback styles
            if hasattr(module, "fallbacks"):
                fallback_entries.extend(module.fallbacks)
            elif hasattr(module, "entries"):
                fallback_entries.extend(module.entries)
    return fallback_entries


def match_fallback(user_input, fallback_entries):
    query = user_input.strip().lower()
    for entry in fallback_entries:
        for pattern in entry.get("patterns", []):
            if re.search(pattern.lower(), query):
                return entry["response"]
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a test question as an argument.")
        sys.exit(1)

    user_question = sys.argv[1]
    fallback_folder = "Yellowstone_Fallbacks"
    fallback_entries = load_fallback_modules(fallback_folder)

    match = match_fallback(user_question, fallback_entries)

    if match:
        print("Matched response:\n")
        print(match)
    else:
        print("No match found for that question.")
