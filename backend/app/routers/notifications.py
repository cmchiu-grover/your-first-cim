from fastapi import APIRouter, Request
from backend.app.models.notification import NotificationCreate
from backend.app.services import notifications_service

router = APIRouter()

@router.get("/api/notifications")
async def get_notifications(request: Request):
    return await notifications_service.get_my_notifications(request)

@router.put("/api/notifications/mark_read")
async def mark_read(request: Request):
    return await notifications_service.mark_all_read(request)

@router.post("/api/notifications/create")
async def create_notification(data: NotificationCreate):
    return await notifications_service.create_notification(data)
