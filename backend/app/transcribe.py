import boto3, asyncio, struct
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

class ResultHandler(TranscriptResultStreamHandler):
    def __init__(self, *args):
        super().__init__(*args)
        self.transcript = ""

    async def handle_transcript_event(self, event: TranscriptEvent):
        for result in event.transcript.results:
            if not result.is_partial:
                self.transcript += " ".join(
                    alt.transcript
                    for alt in result.alternatives
                )

async def transcribe_audio(pcm_bytes: bytes) -> str:
    """Send Float32 PCM (16kHz mono) to AWS Transcribe, get text back."""
    client = TranscribeStreamingClient(region="us-east-1")
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )
    handler = ResultHandler(stream.output_stream)

    async def send_audio():
        # Send in 200ms chunks (6400 bytes at 16kHz 16-bit)
        chunk_size = 6400
        for i in range(0, len(pcm_bytes), chunk_size):
            await stream.input_stream.send_audio_event(
                audio_chunk=pcm_bytes[i:i+chunk_size]
            )
        await stream.input_stream.end_stream()

    await asyncio.gather(send_audio(), handler.handle_events())
    return handler.transcript.strip()
