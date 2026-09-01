from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from backend.app.services import sse_service

router = APIRouter()

@router.get("/sse/standard_time")
async def sse_standard_time(request: Request):
    return StreamingResponse(sse_service.stream_standard_time_updates(request), media_type="text/event-stream")

@router.get("/api/notifications/unread")
async def get_unread_notifications(request: Request):
    return await sse_service.get_unread_notifications(request)
