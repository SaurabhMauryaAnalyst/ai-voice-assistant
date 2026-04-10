import os
import json
import redis
import asyncio

# Redis connection
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

SESSION_TTL = 3600   # session expires after 1 hour


async def get_history(session_id: str):
    """
    Fetch conversation history from Redis.
    Returns list of messages formatted for Claude API.
    """

    loop = asyncio.get_event_loop()

    data = await loop.run_in_executor(
        None,
        redis_client.get,
        f"session:{session_id}"
    )

    if not data:
        return []

    try:
        return json.loads(data)
    except Exception:
        return []


async def append_history(session_id: str, user_text: str, assistant_text: str):
    """
    Append a new conversation turn to Redis history.
    """

    history = await get_history(session_id)

    history.append({
        "role": "user",
        "content": user_text
    })

    history.append({
        "role": "assistant",
        "content": assistant_text
    })

    loop = asyncio.get_event_loop()

    await loop.run_in_executor(
        None,
        redis_client.setex,
        f"session:{session_id}",
        SESSION_TTL,
        json.dumps(history)
    )