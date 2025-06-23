# YellowRoam Chat Logic Engine: Functions 81–160


# === Alert Prioritization & Environmental Factors ===

def prioritize_weather_alerts(alerts: list) -> list:
    """Sorts alerts from most to least critical."""
    priority = {"blizzard": 1, "avalanche": 2, "road closure": 3, "wind": 4, "air quality": 5}
    return sorted(alerts, key=lambda x: priority.get(x.lower(), 99))

def detect_weather_conflict(prompt: str) -> bool:
    """Checks if weather-sensitive activity is mentioned during hazardous season."""
    return "camp" in prompt.lower() and any(word in prompt.lower() for word in ["storm", "snow", "ice"])

def rate_alert_severity(alert: str) -> int:
    """Returns numerical severity rating for known alert types."""
    levels = {"watch": 1, "advisory": 2, "warning": 3}
    for level in levels:
        if level in alert.lower():
            return levels[level]
    return 0

def flag_flash_flood_zone(area: str) -> bool:
    """Identifies if location is in flash flood zone."""
    return area.lower() in ["lamar valley", "madison", "norris geyser basin"]

def recommend_indoor_options(weather: str) -> list:
    """Recommends indoor options for inclement weather."""
    if weather.lower() in ["rain", "snow", "wind"]:
        return ["Albright Visitor Center", "Museum of the National Park Ranger", "Bozeman Museum of the Rockies"]
    return []

# === User Behavior Tuning ===

def detect_frequent_traveler(history: list) -> bool:
    """Returns True if user has 3+ recorded travel sessions."""
    return len(history) >= 3

def track_user_language_usage(session_data: dict) -> str:
    """Returns most commonly used language."""
    return session_data.get("preferred_lang", "en")

def log_user_feedback(prompt: str, rating: int) -> str:
    """Logs user sentiment based on rating."""
    return f"User rated: {rating}/5 for: '{prompt}'"

def flag_uncertain_input(prompt: str) -> bool:
    """Returns True if user's prompt includes uncertainty."""
    return any(q in prompt.lower() for q in ["maybe", "not sure", "i guess"])

def boost_response_for_enthusiasm(prompt: str) -> str:
    """Adds excitement if user shows enthusiasm."""
    if "can't wait" in prompt.lower():
        return "Awesome! You're going to have an unforgettable time! " + prompt
    return prompt

# === Emergency Escalation Support ===

def is_high_priority_emergency(prompt: str) -> bool:
    """Detects life-threatening language."""
    return any(term in prompt.lower() for term in ["injured", "bleeding", "lost", "attacked"])

def escalate_to_emergency_contacts(location: str) -> str:
    """Suggests nearest ranger or emergency number."""
    return f"For emergencies in {location.title()}, dial 911 or contact the nearest ranger station."

def offer_offline_emergency_tips() -> list:
    """Offline survival basics when no signal is available."""
    return ["Stay put if lost", "Signal with reflective objects", "Conserve phone battery", "Use whistle or mirror"]

def assess_signal_blackspots(location: str) -> bool:
    """Identifies if area is a known cell dead zone."""
    return location.lower() in ["tower junction", "bechler", "pelican valley", "specimen ridge"]

def recommend_satellite_device(user_tier: str) -> bool:
    """Suggests GPS beacon if user is on pro or higher tier."""
    return user_tier in ["pro", "lifetime"]

# === Mood & Sentiment Analysis ===

def analyze_sentiment(prompt: str) -> str:
    """Returns mood: 'positive', 'neutral', or 'negative'."""
    if any(word in prompt.lower() for word in ["love", "amazing", "excited"]):
        return "positive"
    elif any(word in prompt.lower() for word in ["hate", "worried", "nervous"]):
        return "negative"
    return "neutral"

def adjust_response_tone(mood: str, message: str) -> str:
    """Tunes tone to match user's sentiment."""
    if mood == "positive":
        return "Great to hear! " + message
    if mood == "negative":
        return "Thanks for letting us know. " + message
    return message

def suggest_decompression(prompt: str) -> list:
    """Suggests relaxing activities if user sounds overwhelmed."""
    if any(w in prompt.lower() for w in ["overwhelmed", "too much", "burnout"]):
        return ["Scenic drive", "Hot springs", "Easy nature trail"]
    return []

def detect_joke_or_irony(prompt: str) -> bool:
    """Flags potential sarcasm or humor."""
    return any(symbol in prompt for symbol in ["😂", "lol", "jk", "just kidding"])

def thank_user_for_feedback(prompt: str) -> str:
    """Generates a default thank-you note."""
    return f"Thanks for your message about: '{prompt}' — we appreciate it."

# === Geographical Intelligence ===

def get_nearest_highpoint(location: str) -> str:
    """Returns nearby scenic high elevation."""
    if "bozeman" in location.lower():
        return "Hyalite Peak"
    if "west yellowstone" in location.lower():
        return "Lone Mountain"
    return "Mount Washburn"

def suggest_photography_times(month: int) -> str:
    """Returns optimal lighting windows."""
    if month in [6, 7, 8]:
        return "Best photo light: 6:30 AM to 8:30 AM and 6 PM to 8 PM"
    return "Golden hour is 1 hour after sunrise and before sunset"

def offer_elevation_rationale(activity: str) -> str:
    """Gives reason why elevation matters for this activity."""
    if "bike" in activity.lower():
        return "High elevations reduce oxygen—go slow and hydrate."
    if "fish" in activity.lower():
        return "Cold alpine lakes at elevation support native trout."
    return ""

def list_all_gateway_towns() -> list:
    """Returns full list of towns surrounding Yellowstone."""
    return ["Gardiner", "Cooke City", "West Yellowstone", "Cody", "Jackson", "Driggs"]

def suggest_offseason_visits(current_month: int) -> str:
    """Suggests low-crowd months."""
    if current_month in [4, 10, 11]:
        return "Visit in spring or fall to avoid peak crowds and enjoy solitude."
    return "Summer is busier but also fully accessible."

# === End of Functions 81–160 ===
