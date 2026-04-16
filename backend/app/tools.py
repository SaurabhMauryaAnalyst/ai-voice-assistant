import requests
import wikipedia
from datetime import datetime

# -------- DATE / TIME --------

def get_date():
    return datetime.now().strftime("Today is %A, %d %B %Y.")

def get_time():
    return datetime.now().strftime("The time is %I:%M %p.")


# -------- WEATHER --------

def get_bangalore_weather():

    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=12.9716&longitude=77.5946&current_weather=true"

        r = requests.get(url)
        data = r.json()

        temp = data["current_weather"]["temperature"]

        return f"The current temperature in Bangalore is {temp} degrees Celsius."

    except:
        return "Sorry, I couldn't fetch the weather."


# -------- CALCULATOR --------

def calculate_math(query):

    try:
        expression = query.replace("calculate", "").strip()

        result = eval(expression)

        return f"The result is {result}"

    except:
        return None


# -------- WIKIPEDIA --------

def wikipedia_search(query):

    try:
        result = wikipedia.summary(query, sentences=2)
        return result

    except:
        return None


# -------- GOOGLE SEARCH --------

def google_search(query):

    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        r = requests.get(url)
        data = r.json()

        return data.get("AbstractText", "")

    except:
        return None