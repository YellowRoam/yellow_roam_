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
