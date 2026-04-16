import redis
import json
import os
import asyncio

# Detect environment
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)

SESSION_TTL = 3600


async def get_history(session):

    try:
        loop = asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            redis_client.get,
            f"session:{session}"
        )

        if not data:
            return []

        return json.loads(data)

    except Exception as e:
        print("Redis read error:", e)
        return []


async def append_history(session, user, assistant):

    try:
        history = await get_history(session)

        history.append({"role": "user", "content": user})
        history.append({"role": "assistant", "content": assistant})

        loop = asyncio.get_event_loop()

        await loop.run_in_executor(
            None,
            redis_client.setex,
            f"session:{session}",
            SESSION_TTL,
            json.dumps(history)
        )

    except Exception as e:
        print("Redis write error:", e)