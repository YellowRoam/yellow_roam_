
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
client = openai
logger = logging.getLogger("YellowRoam")

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

profanity_block = re.compile(r"\b(hell|damn|shit|fuck|bitch)\b", re.IGNORECASE)
