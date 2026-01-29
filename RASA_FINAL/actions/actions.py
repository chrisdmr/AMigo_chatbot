import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
import urllib.parse
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import xml.etree.ElementTree as ET
import country_converter as coco


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher, tracker, domain):
        weather = tracker.get_slot("weather")
        if not weather:
            possible_weathers = ["snowy", "sunny", "rainy"]
            weather = random.choice(possible_weathers)
            dispatcher.utter_message(text=f"It's {weather} today.")
            return [SlotSet("weather", weather)]
        else:
            dispatcher.utter_message(text=f"The weather is still {weather} today.")
            return []

class ActionSuggestActivity(Action):

    def name(self) -> Text:
        return "action_suggest_activity"

    def run(self, dispatcher, tracker, domain):

        weather = tracker.get_slot("weather")

        if not weather:
            possible_weathers = ["snowy", "sunny", "rainy"]
            weather = random.choice(possible_weathers)
            SlotSet("weather", weather)

        activities = {
            "snowy": ["stay inside and read a book, go skiing, or make a snowman"],
            "sunny": ["go for a walk, have a picnic, or arrange a coffee date with a friend"],
            "rainy": ["watch a movie, visit a museum, or take a relaxing bath"]
        }

        suggestion = random.choice(activities[weather])

        dispatcher.utter_message(
            text=f"Since it's {weather} out, you can {suggestion}."
        )

        return [SlotSet("weather", weather)]

import requests

class ActionMorningBriefing(Action):

    def name(self):
        return "action_morning_briefing"

    def run(self, dispatcher, tracker, domain):

        try:
            country = tracker.get_slot ("country")
            category = tracker.get_slot ("category")
            api_key = "pub_1b4df2e8693041ed9b2beac9e9c86a1b"

            print("RAW SLOT country:", country)
            print("USER MESSAGE:", tracker.latest_message.get("text"))

            if not country:
                dispatcher.utter_message(
                    "Country not found. Please provide a valid country along with the news domain you're interested in."
                )
                return [SlotSet("country", None), SlotSet("category", None)]

            country_code = coco.convert(names=country, to='ISO2')

            if country_code == "not found":
                dispatcher.utter_message(text=f"I'm sorry, I don't recognize the country '{country}'. Please provide a valid country along with the news domain you're interested in.")
                return [SlotSet("country", None), SlotSet("category", None)]

            if not category:
                dispatcher.utter_message(text=f"Sorry, invalid/missing category. I'll search for the top news instead.")
                category = "top"

            print("COUNTRY CODE:", country_code)
            print("CATEGORY:", category)
            url = f"https://newsdata.io/api/1/news?apikey={api_key}&country={country_code}&category={category}"
            print("URL USED:", url)

            response = requests.get(url)
            data = response.json()

            for article in data.get('results', [])[:3]:
                title = article.get('title')
                dispatcher.utter_message(text=f"{title}")
            return [SlotSet("country", None), SlotSet("category", None)]


        except Exception:
            dispatcher.utter_message(response="utter_briefing_error")
            return [SlotSet("country", None), SlotSet("category", None)]

        # return []

class ActionSuggestOutfit(Action):

    def name(self):
        return "action_suggest_outfit"

    def run(self, dispatcher, tracker, domain):

        print("\nOUTFIT DEBUGGING START")
        city = tracker.get_slot("city")
        print("RAW SLOT city:", city)
        print("USER MESSAGE:", tracker.latest_message.get("text"))

        if not city:
            dispatcher.utter_message(
                "City not found. Please provide a major city."
            )
            return []

        formatted_city = urllib.parse.quote(city.replace(" ", "_"))

        print("FORMATTED CITY:", formatted_city)
        url = f"https://wttr.in/{formatted_city}?format=j1"
        print("URL USED:", url)

        try:

            data = requests.get(url, timeout=10).json()

            current = data["current_condition"][0]

            temp = int(current["temp_C"])
            desc = current["weatherDesc"][0]["value"].lower()

            if temp < 8:
                outfit = "a warm sweater and coat, a scarf, and a pair of gloves"
            elif temp < 15:
                outfit = "dark wash jeans and a leather jacket or a hoodie"
            elif temp < 25:
                outfit = "a T-shirt and baggy jeans or chinos"
            else:
                outfit = "summer clothes, like a sundress or a linen shirt and shorts"

            if "rain" in desc or "cloudy" in desc or "drizzle" in desc:
                outfit += ". Don't forget your umbrella"

            dispatcher.utter_message(
                text=f"In {city} it's {temp}°C and the weather description is {desc}. I suggest {outfit}."
            )
            print("DEBUG: Clearing city slot for next turn.")
            return [SlotSet("city", None)]

        except Exception as e:
            print(f"ACTION ERROR: {e}")
            dispatcher.utter_message(response="utter_outfit_error")
            return [SlotSet("city", None)]


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="I’m sorry, but I'm not sure how to answer that. Try asking me about the weather, recommended activities and outfits, or today's news!"
        )
        return []




