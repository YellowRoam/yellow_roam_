import sys
from prototype.load_logic import load_language_logic_map
from prototype.response_handler import get_local_response

def run_interactive_matcher():
    print("🟡 YellowRoam Local Logic Matcher")
    print("Type 'exit' to quit.\n")

    # Load all Python-based fallback logic modules
    logic_map = load_language_logic_map()

    language = "en"
    tier = "free"
    park = "Yellowstone"
    region = "lake"  # Update this as needed for different areas

    while True:
        prompt = input("💬 Enter a prompt: ").strip()
        if prompt.lower() in {"exit", "quit"}:
            break

        response = get_local_response(
            prompt=prompt,
            language=language,
            tier=tier,
            logic_map=logic_map,
            park=park,
            region=region
        )

        print("🟢 Matched Response:")
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    try:
        run_interactive_matcher()
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
