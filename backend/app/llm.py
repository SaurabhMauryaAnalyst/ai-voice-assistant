import requests
import asyncio

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are a voice assistant.

Rules:
- Speak in short sentences.
- Maximum 15 words.
- Do not hallucinate facts.
- If unsure, say you don't know.
"""


async def stream_llm_response(user_text, history):

    prompt = SYSTEM_PROMPT + "\n\nUser: " + user_text + "\nAssistant:"

    loop = asyncio.get_event_loop()

    def call_ollama():

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 30,
                        "top_p": 0.8
                    }
                },
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            text = data.get("response", "").strip()

            # hard limit sentences
            text = text.split(".")[0] + "."

            return text

        except Exception as e:
            print("Ollama error:", e)
            return "Sorry, I couldn't answer that."

    result = await loop.run_in_executor(None, call_ollama)

    yield result