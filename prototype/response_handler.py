import logging
import os
import openai
import random
import re

from prototype.bozeman_local_tips import (
    restaurant_tips as bozeman_restaurants,
    campground_tips as bozeman_campgrounds,
    hiking_tips as bozeman_hiking,
    wildlife_tips as bozeman_wildlife,
    winter_tips as bozeman_winter
)
from prototype.jackson_local_tips import (
    restaurant_tips as jackson_restaurants,
    campground_tips as jackson_campgrounds,
    hiking_tips as jackson_hiking,
    wildlife_tips as jackson_wildlife,
    winter_tips as jackson_winter
)
from prototype.livingston_local_tips import (
    restaurant_tips as livingston_restaurants,
    campground_tips as livingston_campgrounds,
    hiking_tips as livingston_hiking,
    wildlife_tips as livingston_wildlife,
    winter_tips as livingston_winter
)
from prototype.gardiner_local_tips import (
    restaurant_tips as gardiner_restaurants,
    campground_tips as gardiner_campgrounds,
    hiking_tips as gardiner_hiking,
    wildlife_tips as gardiner_wildlife,
    winter_tips as gardiner_winter
)
from prototype.west_yellowstone_local_tips import (
    restaurant_tips as west_restaurants,
    campground_tips as west_campgrounds,
    hiking_tips as west_hiking,
    wildlife_tips as west_wildlife,
    winter_tips as west_winter
)
from prototype.grand_teton_local_tips import (
    restaurant_tips as teton_restaurants,
    campground_tips as teton_campgrounds,
    hiking_tips as teton_hiking,
    wildlife_tips as teton_wildlife,
    winter_tips as teton_winter
)
from prototype.driggs_grand_targhee_local_tips import (
    restaurant_tips as driggs_restaurants,
    campground_tips as driggs_campgrounds,
    hiking_tips as driggs_hiking,
    wildlife_tips as driggs_wildlife,
    winter_tips as driggs_winter
)
from prototype.yellowstone_weather_tips import stard_tips as weather_tips
from prototype.yellowstone_local_tips import stard_tips as yellowstone_tips
from prototype.yellowstone_system_prompt import system_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")
logger = logging.getLogger("YellowRoam")
logger.setLevel(logging.INFO)

profanity_block = re.compile(r"\b(hell|damn|shit|fuck|bitch)\b", re.IGNORECASE)

location_categories = {
    "bozeman": {
        "restaurant": bozeman_restaurants,
        "campground": bozeman_campgrounds,
        "hiking": bozeman_hiking,
        "wildlife": bozeman_wildlife,
        "winter": bozeman_winter
    },
    "jackson": {
        "restaurant": jackson_restaurants,
        "campground": jackson_campgrounds,
        "hiking": jackson_hiking,
        "wildlife": jackson_wildlife,
        "winter": jackson_winter
    },
    "livingston": {
        "restaurant": livingston_restaurants,
        "campground": livingston_campgrounds,
        "hiking": livingston_hiking,
        "wildlife": livingston_wildlife,
        "winter": livingston_winter
    },
    "gardiner": {
        "restaurant": gardiner_restaurants,
        "campground": gardiner_campgrounds,
        "hiking": gardiner_hiking,
        "wildlife": gardiner_wildlife,
        "winter": gardiner_winter
    },
    "west yellowstone": {
        "restaurant": west_restaurants,
        "campground": west_campgrounds,
        "hiking": west_hiking,
        "wildlife": west_wildlife,
        "winter": west_winter
    },
    "grand teton": {
        "restaurant": teton_restaurants,
        "campground": teton_campgrounds,
        "hiking": teton_hiking,
        "wildlife": teton_wildlife,
        "winter": teton_winter
    },
    "driggs": {
        "restaurant": driggs_restaurants,
        "campground": driggs_campgrounds,
        "hiking": driggs_hiking,
        "wildlife": driggs_wildlife,
        "winter": driggs_winter
    }
}

weather_keywords = ["weather", "storm", "wind", "snow", "hail", "lightning", "sun", "cold", "hot", "temperature"]

def _run_gpt_with_local_flavor(prompt):
    try:
        logger.info(f"Calling GPT-4 fallback for prompt: {prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        if content:
            return content
        else:
            logger.warning("GPT-4 fallback returned empty content.")
            return "We couldn’t generate a full response just now, but we’re live and taking questions about Yellowstone. Try rephrasing or ask something else — we’re here to help."
    except Exception as e:
        logger.exception("GPT fallback failed — exception occurred.")
        return "We couldn’t generate a full response due to a system error. Please try again shortly."

def _looks_like_yellowstone_prompt(prompt):
    ecosystem_keywords = [
        "yellowstone", "lamar", "hayden", "mammoth", "geyser", "bison", "elk", "hot spring",
        "old faithful", "canyon", "fishing bridge", "tower", "mud volcano", "slough creek",
        "roosevelt", "grand prismatic", "norris", "wildlife", "bear", "bozeman", "gardiner",
        "jackson hole", "jackson", "livingston", "driggs", "grand teton", "tetons",
        "fly fishing", "paradise valley", "cody", "chief joseph highway", "big sky",
        "west yellowstone", "grand targhee", "targhee national forest", "hebgen lake",
        "gallatin national forest", "teton village", "big sky resort", "rodeo", "madison river",
        "snake river", "whitewater rafting", "gallatin river", "tubing", "hiking shoes",
        "camping gear", "backcountry skiing", "cooke city", "south entrance", "north entrance",
        "west entrance", "moose", "ski jackson hole", "ski big sky", "ski bridger bowl",
        "snowcoach", "snowmobiling"
    ]
    return any(kw in prompt for kw in ecosystem_keywords)

def respond(prompt, user_id, location, tier, language, region):
    if profanity_block.search(prompt):
        return "Please keep it respectful — we’re here to help with local Yellowstone questions."

    lowered_prompt = prompt.lower()
    lowered_location = location.lower()

    if any(word in lowered_prompt for word in weather_keywords):
        return random.choice(weather_tips)

    local_tip = ""
    matched_category = None

    for key in location_categories:
        if key in lowered_location:
            for category in location_categories[key]:
                if category in lowered_prompt:
                    matched_category = category
                    local_tip = random.choice(location_categories[key][category])
                    break
            break

    if _looks_like_yellowstone_prompt(lowered_prompt):
        gpt_response = _run_gpt_with_local_flavor(prompt)
        if local_tip:
            return f"{gpt_response}\n\n★ Local Tip ({matched_category.title()}): {local_tip}"
        return gpt_response

    return "That’s outside of our service area. We only answer questions about the Yellowstone ecosystem and the area."

        
        
        
