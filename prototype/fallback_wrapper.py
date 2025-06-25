# prototype/fallback_wrapper.py

from prototype.chat_logic import chat_router


def handle_user_prompt(user_input, user_tier="free", language="en"):
    """
    Handles a user prompt using either fallback logic or an upgraded router.
    """
    result = chat_router(user_input, user_tier=user_tier, language=language)

    if result:
        return result

    return "⚠️ Sorry, I couldn’t find a matching response. Try rephrasing?"
