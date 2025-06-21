
"""YellowRoam Chat Logic Engine

This module supports:
- Context awareness
- Intent routing
- Prompt restructuring
- Seasonal/geographic adjustments
- Tier-specific logic
- Multilingual and behavioral response tuning
"""

import json
from datetime import datetime


# === Intent & Topic Detection ===

def is_yellowstone_weather_request(prompt: str) -> bool:
    """Determines if the prompt is about Yellowstone weather."""
    keywords = ["yellowstone", "weather", "forecast", "climate", "snow", "temperature"]
    return any(k in prompt.lower() for k in keywords)


def is_trail_request(prompt: str) -> bool:
    """Detects if the user is asking about hiking or trails."""
    keywords = ["trail", "hike", "path", "walk", "trek"]
    return any(k in prompt.lower() for k in keywords)


def is_dining_request(prompt: str) -> bool:
    """Determines if the user is asking about restaurants, food, or dining."""
    keywords = ["restaurant", "food", "dining", "eat", "cafe", "coffee", "breakfast"]
    return any(k in prompt.lower() for k in keywords)


def is_family_friendly_request(prompt: str) -> bool:
    """Detects interest in kid-friendly or family-oriented activities."""
    keywords = ["kid", "family", "children", "child", "toddler"]
    return any(k in prompt.lower() for k in keywords)


def is_pet_friendly_request(prompt: str) -> bool:
    """Checks if the prompt includes pet-related travel concerns."""
    keywords = ["pet", "dog", "cat", "animal", "pet-friendly"]
    return any(k in prompt.lower() for k in keywords)


def is_subscription_upgrade_request(prompt: str) -> bool:
    """Detects if the user is asking about pricing or subscription tiers."""
    keywords = ["upgrade", "subscription", "pricing", "plan", "cost", "tier"]
    return any(k in prompt.lower() for k in keywords)


def is_weather_alert_request(prompt: str) -> bool:
    """Detects requests for alerts such as storms, road closures, or avalanche warnings."""
    keywords = ["alert", "warning", "storm", "avalanche", "closure", "snow", "blizzard"]
    return any(k in prompt.lower() for k in keywords)


def is_travel_planning_request(prompt: str) -> bool:
    """Checks if the user is asking for help planning a trip or itinerary."""
    keywords = ["plan", "trip", "itinerary", "route", "travel"]
    return any(k in prompt.lower() for k in keywords)


def is_event_schedule_request(prompt: str) -> bool:
    """Detects interest in events like rodeos, festivals, or farmers markets."""
    keywords = ["event", "festival", "rodeo", "schedule", "market"]
    return any(k in prompt.lower() for k in keywords)


def is_glamping_or_lodging_request(prompt: str) -> bool:
    """Detects lodging-related queries including glamping and cabins."""
    keywords = ["glamping", "camping", "lodging", "motel", "cabin", "hotel", "stay"]
    return any(k in prompt.lower() for k in keywords)


# === Location & Context Routing ===

def route_to_yellowstone_logic(location: str) -> str:
    """Routes to Yellowstone logic file if location matches."""
    if "yellowstone" in location.lower():
        return "logic/yellowstone_weather_logic.json"
    return "logic/fallback_logic.json"

def route_to_bozeman_logic(location: str) -> str:
    """Routes to Bozeman logic."""
    if "bozeman" in location.lower():
        return "logic/bozeman.logic.json"
    return "logic/fallback_logic.json"

def route_to_big_sky_logic(location: str) -> str:
    """Routes to Big Sky logic."""
    if "big sky" in location.lower():
        return "logic/big_sky.logic.json"
    return "logic/fallback_logic.json"

def route_to_west_yellowstone_logic(location: str) -> str:
    """Routes to West Yellowstone logic."""
    if "west yellowstone" in location.lower():
        return "logic/west_yellowstone_weather_logic.json"
    return "logic/fallback_logic.json"

def route_to_grand_teton_logic(location: str) -> str:
    """Routes to Grand Teton logic."""
    if "grand teton" in location.lower():
        return "logic/jackson_drggs.logic.json"
    return "logic/fallback_logic.json"

def is_location_supported(location: str) -> bool:
    """Checks if the location is among supported areas."""
    supported = ["yellowstone", "bozeman", "big sky", "west yellowstone", "jackson", "driggs"]
    return any(loc in location.lower() for loc in supported)

def get_elevation_by_location(location: str) -> int:
    """Returns approximate elevation in feet."""
    elevation_map = {
        "bozeman": 4800,
        "yellowstone": 7500,
        "mammoth": 6200,
        "old faithful": 7300,
        "cody": 6600,
        "south entrance": 6900,
        "jackson": 6200
    }
    return elevation_map.get(location.lower(), 6000)

def get_region_by_gate(location: str) -> str:
    """Returns region name from park gate.", e.g., north, south, east."""
    if "gardiner" in location.lower():
        return "north entrance"
    if "cody" in location.lower():
        return "east entrance"
    if "south entrance" in location.lower():
        return "south entrance"
    return "unknown region"

def is_backcountry_area(location: str) -> bool:
    """Detects if location is remote or alpine."""
    return any(x in location.lower() for x in ["slough creek", "eagle peak", "pelican valley", "specimen ridge"])

def get_nearest_weather_station(location: str) -> str:
    """Returns likely weather reference station."""
    if "lake" in location.lower():
        return "Yellowstone Lake NOAA Station"
    elif "canyon" in location.lower():
        return "Canyon Village SNOTEL"
    return "Old Faithful Geyser Basin"

# === Seasonal & Environmental Adjustments ===

def adjust_prompt_by_month(prompt: str, month: int) -> str:
    """Injects seasonal context into weather-related prompts."""
    if month in [12, 1, 2]:
        return f"{prompt} Be aware it's full winter in Yellowstone."
    if month in [6, 7, 8]:
        return f"{prompt} Expect wildfires and afternoon storms in summer."
    if month in [3, 4, 5]:
        return f"{prompt} Conditions may include snowpack and road closures."
    if month in [9, 10, 11]:
        return f"{prompt} Fall brings elk rut and early snowfall."
    return prompt

def is_snow_season(month: int) -> bool:
    """Returns True if current month is typically snowy."""
    return month in [10, 11, 12, 1, 2, 3]

def get_current_season(date: datetime) -> str:
    """Returns the current Yellowstone season."""
    m = date.month
    if m in [12, 1, 2]:
        return "winter"
    if m in [3, 4, 5]:
        return "spring"
    if m in [6, 7, 8]:
        return "summer"
    if m in [9, 10, 11]:
        return "fall"

def add_layering_advice(season: str) -> str:
    """Returns clothing advice based on season."""
    if season == "winter":
        return "Wear thermal layers, insulated boots, and wind protection."
    if season == "summer":
        return "Pack sunscreen, rain gear, and extra water."
    if season == "spring":
        return "Conditions vary—bring waterproof shoes and layers."
    if season == "fall":
        return "Expect frost. Bring gloves, a hat, and warm layers."
    return ""

def is_lightning_likely(month: int) -> bool:
    """Returns True if month has higher lightning frequency."""
    return month in [6, 7, 8]

# === Subscription Tier Filtering ===

def check_user_tier_access(tier: str, feature: str) -> bool:
    """Returns True if the user tier grants access to feature."""
    access_map = {
        "free": ["basic weather", "trail status"],
        "explorer": ["basic weather", "trail status", "dining", "lodging"],
        "pro": ["everything", "priority alerts"],
        "lifetime": ["everything"]
    }
    allowed = access_map.get(tier, [])
    return "everything" in allowed or feature in allowed

def filter_results_by_subscription(tier: str, results: list) -> list:
    """Returns filtered results based on user tier."""
    if tier == "free":
        return results[:3]
    if tier == "explorer":
        return results[:10]
    return results

def tier_label(tier: str) -> str:
    """Returns human-readable tier label."""
    labels = {
        "free": "Free Plan",
        "explorer": "Explorer Plan",
        "pro": "Pro Plan",
        "lifetime": "Lifetime Access"
    }
    return labels.get(tier.lower(), "Unknown Plan")

def should_show_premium_message(tier: str) -> bool:
    """Returns True if user is on free plan and feature is gated."""
    return tier == "free"

def explain_tier_benefits(tier: str) -> str:
    """Returns a description of what the user's plan includes."""
    if tier == "free":
        return "Access to basic features like weather and trails."
    if tier == "explorer":
        return "Includes lodging, dining, and activity filters."
    if tier == "pro":
        return "Pro tools, alerts, and route planner access."
    if tier == "lifetime":
        return "Full access forever. Thank you for supporting us!"

# === Multilingual & Accessibility Support ===

def apply_language_logic(prompt: str, lang: str) -> str:
    """Returns the prompt translated or formatted for the given language."""
    translations = {
        "es": "Traducido al español",
        "fr": "Traduit en français",
        "hi": "हिंदी में अनुवादित",
        "sv": "Översatt till svenska"
    }
    return f"{translations.get(lang, '')}: {prompt}"

def is_supported_language(lang: str) -> bool:
    """Checks if language is supported in YellowRoam."""
    return lang.lower() in ["en", "es", "fr", "hi", "sv"]

def language_display_name(lang: str) -> str:
    """Returns readable language name."""
    return {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "hi": "Hindi",
        "sv": "Swedish"
    }.get(lang.lower(), "Unknown Language")

def get_default_language(user_settings: dict) -> str:
    """Returns the default language for a user."""
    return user_settings.get("language", "en")

def should_translate_prompt(user_settings: dict) -> bool:
    """Returns True if translation should be applied."""
    return user_settings.get("translate", False)


# === Prompt Rewriting & Enhancement ===

def rephrase_for_clarity(prompt: str) -> str:
    """Attempts to clarify vague questions."""
    if "best time" in prompt:
        return prompt + " — are you asking about weather, crowds, or cost?"
    if "where should I go" in prompt:
        return prompt + " — are you looking for trails, views, or wildlife?"
    return prompt

def strip_noise_words(prompt: str) -> str:
    """Cleans filler from input (e.g., 'please', 'um', etc)."""
    noise = ["please", "um", "uh", "i mean", "you know"]
    for word in noise:
        prompt = prompt.replace(word, "")
    return prompt.strip()

def capitalize_prompt(prompt: str) -> str:
    """Ensures prompt starts with capital letter."""
    return prompt[0].upper() + prompt[1:] if prompt else prompt

def simplify_prompt_for_translation(prompt: str) -> str:
    """Reduces compound prompts for easier translation."""
    if " and " in prompt:
        return prompt.split(" and ")[0]
    return prompt

def generate_clarification_prompt(original: str) -> str:
    """Suggests a clarification question for user."""
    return f"I'm not quite sure what you meant by: '{original}'. Could you clarify or be more specific?"

def merge_user_followup(prompt: str, followup: str) -> str:
    """Combines user's original message with their clarification."""
    return f"{prompt}. Follow-up clarification: {followup}"

def expand_prompt_with_tags(prompt: str, tags: list) -> str:
    """Appends useful tags to the prompt context."""
    return f"{prompt} [Tags: {', '.join(tags)}]"

def insert_local_seasonal_context(prompt: str, month: int, location: str) -> str:
    """Adds relevant seasonal note into prompt."""
    if location.lower() == "yellowstone" and month in [12, 1, 2]:
        return prompt + " (Expect snow, limited access, and oversnow travel)"
    return prompt

def add_fallback_option(prompt: str) -> str:
    """Adds a fallback 'Did you mean…' line."""
    return prompt + " (Did you mean to ask about weather, wildlife, or lodging?)"

def reroute_to_suggestions(prompt: str) -> str:
    """Directs user to possible suggestions page."""
    return "Let me show you a few options that match your request: " + prompt

# === Data Source + Alert Interfaces ===

def fetch_weather_alerts(location: str) -> list:
    """Stub for real-time weather alert API integration."""
    return [f"⚠️ No current alerts for {location}. (Live data integration pending)"]

def get_snow_depth_estimate(location: str, month: int) -> str:
    """Estimates snow depth for location in given month."""
    if location.lower() == "yellowstone" and month in [1, 2, 3]:
        return "Typical snow depth: 3 to 6 feet"
    return "Snow depth data not available"

def get_trail_status(location: str) -> str:
    """Returns generic trail status (dynamic link optional)."""
    if "yellowstone" in location.lower():
        return "Some trails may be muddy or snow-covered. Check with NPS updates."
    return "Trail conditions vary. Use caution."

def query_fire_risk(zone: str) -> str:
    """Returns fire risk info based on region."""
    return f"Fire risk in {zone.title()} region: Moderate (Check airnow.gov for updates)"

def fetch_avalanche_forecast(region: str) -> str:
    """Stub for avalanche data."""
    return f"Avalanche risk in {region.title()}: Considerable. Visit mtavalanche.com for updates."

def get_road_closure_status(region: str) -> str:
    """Stub for road closure info."""
    return f"Some seasonal roads in {region.title()} may be closed. Check nps.gov for maps."

def generate_air_quality_warning(location: str) -> str:
    """Stub for AQI warning message."""
    return f"Air quality near {location.title()}: Good today (no smoke detected)."

def simulate_live_temp(location: str) -> str:
    """Simulates live temperature output (placeholder)."""
    return f"The current temperature in {location.title()} is approximately 58°F."

def fetch_sunrise_sunset(month: int, location: str) -> str:
    """Rough sunrise/sunset estimate."""
    if month in [6, 7]:
        return f"Sunrise near {location.title()} is around 5:45 AM, sunset 9:15 PM."
    if month in [12, 1]:
        return f"Sunrise is near 7:45 AM, sunset 4:40 PM."
    return "Daylight hours vary seasonally."

def generate_detailed_weather_tip(location: str) -> str:
    """Returns a locally tuned weather advisory."""
    return f"In {location.title()}, storms can form quickly. Carry layers, water, and sun protection at all times."

# === UX Safeguards + Debug & Fallback Logic ===

def null_guard(input_data) -> bool:
    """Prevents failure from null or empty input."""
    return bool(input_data)

def validate_prompt_structure(prompt: str) -> bool:
    """Checks that prompt is a valid string and not blank."""
    return isinstance(prompt, str) and len(prompt.strip()) > 3

def log_prompt_history(user_id: str, prompt: str) -> None:
    """Stores prompt history for user session (stub)."""
    print(f"[LOG] User {user_id} asked: {prompt}")

def trigger_debug_mode(env: str) -> bool:
    """Returns True if system is in debug/test mode."""
    return env == "dev"

def simulate_unavailable_feature(prompt: str) -> str:
    """Returns placeholder for undeployed features."""
    return "This feature is coming soon in a future update."

def fallback_to_manual_route(prompt: str) -> str:
    """Returns fallback message when routing fails."""
    return f"I couldn't find a perfect match for: '{prompt}'. Want help refining your request?"

def default_response_on_error() -> str:
    """Fails gracefully with default message."""
    return "Sorry, something went wrong. Try again or ask in a different way."

def language_fallback_message(lang: str) -> str:
    """Tells user their language isn't supported yet."""
    return f"Language '{lang}' is not yet available. Defaulting to English."

def show_available_locales() -> list:
    """Returns list of supported locales."""
    return ["en", "es", "fr", "hi", "sv"]

def log_system_event(event: str) -> None:
    """Logs backend events (placeholder)."""
    print(f"[SYSTEM] {event}")
