
from fastapi import APIRouter, Request
from backend.app.models.notification import NotificationCreate
from backend.app.db.crud import (
    get_current_active_user,
    create_notification_and_assign_users,
    get_unread_notification_status,
    mark_all_notifications_read
)
from backend.app.db.dbquery import get_all_user_ids, get_one_user_notifications


router = APIRouter()

@router.get("/api/notifications")
async def get_notifications(request: Request):
    user = await get_current_active_user(request)
    user_id = user.get('id')
    
    if not user_id:
        return {"ok": False, "message": "使用者未登入或無效的使用者 ID"}
    
    try:
        notifications = get_one_user_notifications(user_id)
        return {"ok": True, "notifications": notifications}
    except Exception as e:
        print(f"獲取通知時發生錯誤: {e}")
        return {"ok": False, "message": "獲取通知失敗，請稍後再試"}

@router.get("/api/notifications/unread")
async def get_unread(request: Request):
    user = await get_current_active_user(request)
    has_unread = get_unread_notification_status(user.get('id'))
    return {"has_unread": has_unread}

@router.put("/api/notifications/mark_read")
async def mark_read(request: Request):
    try:
        user = await get_current_active_user(request)
        mark_all_notifications_read(user.get('id'))
        return {"ok": True, "message": "所有通知已標記為已讀"}
    except Exception as e:
        print(f"標記所有通知為已讀時發生錯誤: {e}")
        return {"ok": False, "message": "標記失敗，請稍後再試"}
    
@router.post("/api/notifications/create")
async def create_notification(data: NotificationCreate):
    user_ids = get_all_user_ids()
    notif_id = create_notification_and_assign_users(data, user_ids)
    return {"ok": True, "notification_id": notif_id}
