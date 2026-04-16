from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests
import wikipedia

from app.transcribe import transcribe_audio
from app.llm import stream_llm_response
from app.tts import synthesize_speech
from app.session import get_history, append_history

app = FastAPI()

# -------- CORS --------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- HEALTH CHECK --------

@app.get("/health")
def health():
    return {"status": "ok"}


# -------- TOOLS --------

def get_date():
    return datetime.now().strftime("Today is %A, %d %B %Y.")


def get_time():
    return datetime.now().strftime("The time is %I:%M %p.")


def get_bangalore_weather():

    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=12.9716&longitude=77.5946&current_weather=true"

        r = requests.get(url)
        data = r.json()

        temp = data["current_weather"]["temperature"]

        return f"The current temperature in Bangalore is {temp} degrees Celsius."

    except:
        return "Sorry, I couldn't fetch the weather."


def calculate_math(query):

    try:
        expression = query.replace("calculate", "").strip()
        result = eval(expression)

        return f"The result is {result}"

    except:
        return None


def wikipedia_search(query):

    try:
        result = wikipedia.summary(query, sentences=2)
        return result

    except:
        return None


def google_search(query):

    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        r = requests.get(url)
        data = r.json()

        return data.get("AbstractText", "")

    except:
        return None


# -------- VOICE WEBSOCKET --------

@app.websocket("/ws/voice")
async def voice_ws(ws: WebSocket):

    await ws.accept()

    session_id = ws.query_params.get("session")

    print(f"Client connected session={session_id}")

    audio_buffer = bytearray()

    try:

        while True:

            message = await ws.receive()

            if message["type"] == "websocket.disconnect":
                break

            if "bytes" in message and message["bytes"]:
                audio_buffer.extend(message["bytes"])

            if "text" in message and message["text"] == "stop":
                break

    except WebSocketDisconnect:
        print("client disconnected")

    try:

        if not audio_buffer:
            print("no audio received")
            return

        pcm_audio = bytes(audio_buffer)

        print("Transcribing audio...")

        user_text = await transcribe_audio(pcm_audio)

        print("User:", user_text)

        if not user_text:
            return

        history = await get_history(session_id)

        text_lower = user_text.lower()

        response_text = ""

        # -------- DATE --------

        if "date" in text_lower:
            response_text = get_date()

        # -------- TIME --------

        elif "time" in text_lower:
            response_text = get_time()

        # -------- WEATHER --------

        elif "weather" in text_lower and "bangalore" in text_lower:
            response_text = get_bangalore_weather()

        # -------- AI Name --------
        elif "your name" in text_lower or "who are you" in text_lower:
            response_text = "I am your AI voice assistant."
        # -------- CALCULATOR --------

        elif "calculate" in text_lower or any(x in text_lower for x in ["+", "-", "*", "/"]):

            result = calculate_math(user_text)

            if result:
                response_text = result

        # -------- WIKIPEDIA --------

        elif "who is" in text_lower or "what is" in text_lower:

            wiki = wikipedia_search(user_text)

            if wiki:
                response_text = wiki

        # -------- GOOGLE SEARCH --------

        elif "news" in text_lower or "ipl" in text_lower:

            search = google_search(user_text)

            if search:
                response_text = search

        # -------- LLM FALLBACK --------

        if not response_text:

            async for chunk in stream_llm_response(user_text, history):
                response_text += chunk

        print("AI:", response_text)

        await append_history(session_id, user_text, response_text)

        audio = await synthesize_speech(response_text)

        await ws.send_bytes(audio)

    except Exception as e:
        print("pipeline error:", e)

    finally:
        print(f"Cleaning session={session_id}")