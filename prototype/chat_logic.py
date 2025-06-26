
# prototype/chat_logic.py

from prototype.match_local_logic import match_local_logic

def chat_router(user_input, user_tier="free", language="en"):
    """
    Simple router to return fallback logic response.
    This is a stub. Extend this when you add GPT or tiered logic.
    """
    response = match_local_logic(user_input)
    if response:
        return response

    # If no match, return fallback message
    return "🤖 I'm not sure how to answer that yet, but we're working on it!"


# chat_logic.py

# Emergency detection based on simple keyword scan
def is_high_priority_emergency(prompt: str) -> bool:
    emergency_keywords = ["help", "injury", "bear attack", "lost", "fire", "911", "emergency"]
    return any(word in prompt.lower() for word in emergency_keywords)

# Provide emergency escalation guidance
def escalate_to_emergency_contacts(location: str) -> str:
    return f" This sounds serious. Please immediately contact Yellowstone dispatch at 911 or the nearest ranger station in {location}."

# Basic sentiment analysis for tone adjustment
def analyze_sentiment(prompt: str) -> str:
    lower = prompt.lower()
    if any(word in lower for word in ["worried", "frustrated", "angry", "upset", "bad", "terrible"]):
        return "negative"
    elif any(word in lower for word in ["great", "awesome", "excited", "love", "amazing"]):
        return "positive"
    return "neutral"

# Adjust response based on user sentiment
def adjust_response_tone(mood: str, response: str) -> str:
    if mood == "negative":
        return "I'm here to help. " + response
    elif mood == "positive":
        return "Glad you're excited! " + response
    return response

