import pyttsx3
import asyncio
import tempfile

engine = pyttsx3.init()

async def synthesize_speech(text):

    loop = asyncio.get_event_loop()

    def generate():

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:

            path = f.name

        engine.save_to_file(text, path)
        engine.runAndWait()

        with open(path, "rb") as f:
            return f.read()

    return await loop.run_in_executor(None, generate)