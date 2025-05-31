from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from backend.app.db.crud import get_current_active_user
from backend.app.db.dbquery import check_unread_notifications
import asyncio
import redis.asyncio as redis
import os

router = APIRouter()
REDIS_HOST = os.getenv("REDIS_HOST", "redis") 
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379)) 

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@router.get("/sse/standard_time")
async def sse_standard_time(request: Request):
    async def event_generator():
        pubsub = r.pubsub()
        await pubsub.subscribe("standard_time_channel")

        try:
            while True:
                if await request.is_disconnected():
                    break
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    data = message["data"]
                    yield f"data: {data}\n\n"
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            print("SSE connection cancelled.")
        except Exception as e:
            print(f"Error in SSE: {e}")
            yield f"data: {{'error': 'An error occurred: {str(e)}'}}\n\n"
        finally:
            await pubsub.unsubscribe("standard_time_channel")
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/api/notifications/unread")
async def get_unread_notifications(request: Request):
    try:
        user = await get_current_active_user(request)
        print(f"get_unread_notifications: {user}")
        
        rows = check_unread_notifications(int(user.get('id')))
        if not rows:
            print("沒有未讀通知")
            return {"has_unread": False}
        
        else:
            print("有未讀通知")
            return {"has_unread": rows}
    except Exception as e:
        print(f"get_unread_notifications 發生錯誤：{e}")
        return {"error": str(e)}
    
