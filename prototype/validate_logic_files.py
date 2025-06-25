# prototype/validate_logic_files.py

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

        # Validate optional tags
        if "tags" in entry:
            if not isinstance(entry["tags"], list):
                raise ValueError(f"Entry {i}: 'tags' must be a list.")
            if not all(isinstance(tag, str) for tag in entry["tags"]):
                raise ValueError(f"Entry {i}: all 'tags' must be strings.")

        # Validate tier
        if entry["tier"] not in ("free", "pro"):
            raise ValueError(f"Entry {i}: 'tier' must be 'free' or 'pro'.")

    return True
