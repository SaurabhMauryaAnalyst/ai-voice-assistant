import boto3, asyncio
from functools import partial

_polly = boto3.client("polly", region_name="us-east-1")

async def synthesize_speech(text: str) -> bytes | None:
    """Convert text to MP3 using AWS Polly Neural TTS (Matthew voice)."""
    if not text: return None
    loop = asyncio.get_event_loop()

    # Run blocking boto3 call in thread pool
    response = await loop.run_in_executor(
        None,
        partial(
            _polly.synthesize_speech,
            Text=text,
            VoiceId="Matthew",      # or "Joanna", "Aria"
            Engine="neural",         # neural for high quality
            OutputFormat="mp3",
            SampleRate="22050",
        )
    )
    return response["AudioStream"].read()
