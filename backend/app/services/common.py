from backend.app.errors import AppError
from backend.app.models.notification import NotificationCreate
from backend.app.models.redis_pubsub import publish_update
from backend.app.db.crud import create_notification_and_assign_users, assign_posting_user
from backend.app.db.dbquery import get_all_user_ids


def require_login(current_user):
    if not current_user:
        raise AppError(400, "權限不足，請先登入。")
    return current_user


def require_position(current_user, position: str):
    require_login(current_user)
    if current_user.get("position") != position:
        raise AppError(400, f"權限不足，並非 {position} 同仁。")
    return current_user


async def notify_users(current_user, title: str, message: str, event_type: str):
    notif = NotificationCreate(
        title=title,
        message=message,
        event_type=event_type
    )

    user_ids = get_all_user_ids()
    user_id = current_user.get("id")
    user_ids.remove(user_id)
    notif_id = await create_notification_and_assign_users(notif, user_ids)
    await assign_posting_user(user_id, notif_id)

    await publish_update(notif.message, user_id)
