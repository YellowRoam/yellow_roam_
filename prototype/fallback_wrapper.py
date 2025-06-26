
# prototype/fallback_wrapper.py

from prototype.chat_logic import chat_router


def handle_user_prompt(user_input, user_tier="free", language="en"):
    """
    Handles a user prompt using either fallback logic or an upgraded router.
    """
    result = chat_router(user_input, user_tier=user_tier, language=language)

    if result:
        return result

    return " Sorry, I couldn’t find a matching response. Try rephrasing?"

from prototype.chat_logic import (
    is_high_priority_emergency,
    escalate_to_emergency_contacts,
    analyze_sentiment,
    adjust_response_tone
)

def handle_user_prompt(prompt: str, user_id: str = "anonymous", location: str = "Yellowstone") - dict:
    log = []

    if is_high_priority_emergency(prompt):
        escalation = escalate_to_emergency_contacts(location)
        log.append(f"[{datetime.now().isoformat()}] Emergency detected: {prompt}")
        return respond(escalation)

    mood = analyze_sentiment(prompt)
    log.append(f"[{datetime.now().isoformat()}] Mood: {mood}")

    response_text = "Thanks for your question. Let’s dive in."
    adjusted_response = adjust_response_tone(mood, response_text)
    log.append(f"[{datetime.now().isoformat()}] Adjusted response: {adjusted_response}")

    log.append(f"[{datetime.now().isoformat()}] Called mock API for location: {location}")
    log.append(f"[{datetime.now().isoformat()}] Full prompt log from {user_id}: {prompt}")

    return {
        "response": adjusted_response,
        "log": log,
        "timestamp": datetime.now().isoformat()
    }
8ff5b618021ad6232e52060f8bca3fa754ab8ed7
