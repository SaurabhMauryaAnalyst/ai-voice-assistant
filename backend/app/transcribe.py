import os
import whisper
import subprocess
import asyncio
import uuid

print("Loading Whisper model...")
model = whisper.load_model("tiny")   # fastest CPU model
print("Whisper model loaded.")


async def transcribe_audio(audio_bytes):

    try:
        print("Transcribing audio...")

        # create unique filenames
        uid = str(uuid.uuid4())
        webm_path = f"{uid}.webm"
        wav_path = f"{uid}.wav"

        # save audio from browser
        with open(webm_path, "wb") as f:
            f.write(audio_bytes)

        # convert webm → wav using ffmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", webm_path,
                "-ac", "1",
                "-ar", "16000",
                "-vn",
                "-f","wav",
                wav_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        loop = asyncio.get_event_loop()

        result = await loop.run_in_executor(
            None,
            lambda: model.transcribe(
                wav_path,
                language="en",
                fp16=False
            )
        )

        text = result["text"].strip()

        # cleanup temp files
        if os.path.exists(webm_path):
            os.remove(webm_path)

        if os.path.exists(wav_path):
            os.remove(wav_path)



        return text

    except Exception as e:
        print("Transcription error:", e)
        return ""