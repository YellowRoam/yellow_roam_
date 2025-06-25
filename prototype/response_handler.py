import json
import os
import difflib
from rapidfuzz import fuzz, process

# Directory where fallback files are stored
FALLBACK_DIR = "./fallbacks"

# Optional synonym expansion
def expand_synonyms(phrase):
    synonyms = {
        "campground": ["camp site", "camping area", "tent site"],
        "hiking": ["trails", "walking", "trekking"],
        "fishing": ["angling", "fly fishing"],
        "lodging": ["accommodation", "cabin", "hotel"],
        "Jackson": ["Jackson Hole"],
        "Driggs": ["Teton Valley"]
    }
    expanded = [phrase]
    for word, syns in synonyms.items():
        if word in phrase:
            expanded.extend([phrase.replace(word, s) for s in syns])
    return list(set(expanded))



# Core function to find best match using fuzzy matching and synonym expansion
def find_best_fallback(query, fallback_data, threshold=80):
    candidates = []
    queries = expand_synonyms(query.lower())

    for entry in fallback_data:
        for pattern in entry.get("patterns", []):
            for q in queries:
                score = fuzz.partial_ratio(q, pattern.lower())
                if score >= threshold:
                    candidates.append((score, entry))

    if candidates:
        candidates.sort(reverse=True, key=lambda x: x[0])
        return candidates[0][1]  # return best matched entry
    return None

# Main handler function
def handle_query(user_query):
    fallbacks = load_fallback_logic()
    match = find_best_fallback(user_query, fallbacks)
    if match:
        return {
            "response": match["response"],
            "tags": match.get("tags", []),
            "keywords": match.get("keywords", []),
            "match_from": "fallback"
        }
    else:
        return {
            "response": "Sorry, I couldn’t find a match. Try rephrasing your question.",
            "tags": [],
            "match_from": "none"
        }

def respond(entry):
    """
    Return the response string from a matched logic entry.
    """
    if isinstance(entry, dict) and "response" in entry:
        return entry["response"]
    return entry


# Example usage (test locally)
if __name__ == "__main__":
    while True:
        q = input("Ask a Yellowstone/Teton/Driggs question: ")
        result = handle_query(q)
        print("\nResponse:", result["response"])
        print("Tags:", result["tags"])
        print("Keywords:", result["keywords"])
        print("Match Source:", result["match_from"])
        print("\n---\n")
