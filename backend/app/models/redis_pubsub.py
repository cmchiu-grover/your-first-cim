import redis.asyncio as redis
import os
import json

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

async def publish_update(message: str):
    print(f"開始 Publishing update to Redis: {message}")
    await r.publish("standard_time_channel", json.dumps({
        "event": "standard_time_updated",
        "message": message
    }))
