import anthropic, os
from typing import AsyncIterator

client = anthropic.AsyncAnthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

SYSTEM_PROMPT = """You are a knowledgeable, concise voice assistant.
You have broad knowledge across all domains.
Keep answers SHORT and CONVERSATIONAL — you are speaking aloud.
Never use markdown, bullet points, or numbered lists.
Use natural spoken language only."""

async def stream_claude_response(
    user_text: str,
    history: list
) -> AsyncIterator[str]:
    """Stream tokens from Claude claude-sonnet-4-20250514."""
    messages = [
        *history,   # prior turns from Redis
        {"role": "user", "content": user_text}
    ]

    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        async for text in stream.text_stream:
            yield text
