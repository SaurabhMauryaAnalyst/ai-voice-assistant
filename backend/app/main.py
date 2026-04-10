from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio, json, logging
from transcribe import transcribe_audio
from llm        import stream_claude_response
from tts        import synthesize_speech
from session    import get_history, append_history

log = logging.getLogger(__name__)
app = FastAPI(title="AI Voice Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

@app.websocket("/ws/voice")
async def voice_ws(ws: WebSocket, session: str = ""):
    await ws.accept()
    audio_chunks: list[bytes] = []
    stop_event = asyncio.Event()

    try:
        while True:
            # Receive bytes (PCM audio) or text (control messages)
            data = await ws.receive()

            if "bytes" in data:
                audio_chunks.append(data["bytes"])

            elif "text" in data:
                msg = json.loads(data["text"])

                if msg["type"] == "stop":
                    stop_event.set()   # cancel in-flight generation
                    audio_chunks.clear()

                elif msg["type"] == "end_utterance" and audio_chunks:
                    # All audio received — begin pipeline
                    raw_audio = b"".join(audio_chunks)
                    audio_chunks.clear()
                    stop_event.clear()

                    await _process_utterance(
                        ws, raw_audio, session, stop_event
                    )

    except WebSocketDisconnect:
        log.info("Client disconnected session=%s", session)


async def _process_utterance(ws, audio, session_id, stop_event):
    # ── Step 1: Speech → Text ─────────────────────────────────
    transcript = await transcribe_audio(audio)
    await ws.send_json({ "type": "transcript", "text": transcript })

    # ── Step 2: Load history, call Claude ─────────────────────
    history = await get_history(session_id)
    full_reply = ""
    sentence_buf = ""

    async for token in stream_claude_response(transcript, history):
        if stop_event.is_set(): break
        full_reply   += token
        sentence_buf += token

        # ── Step 3: TTS on sentence boundaries ────────────────
        if _is_sentence_boundary(sentence_buf):
            mp3_bytes = await synthesize_speech(sentence_buf.strip())
            if mp3_bytes: await ws.send_bytes(mp3_bytes)
            sentence_buf = ""

    # Flush remaining text
    if sentence_buf.strip() and not stop_event.is_set():
        mp3_bytes = await synthesize_speech(sentence_buf.strip())
        if mp3_bytes: await ws.send_bytes(mp3_bytes)

    # Save conversation turn to Redis
    await append_history(session_id, transcript, full_reply)
    await ws.send_json({ "type": "assistant_done" })


def _is_sentence_boundary(text: str) -> bool:
    return text.rstrip().endswith(('.', '!', '?', ':')) and len(text) > 30
