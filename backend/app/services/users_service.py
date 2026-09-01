from fastapi import Request
from datetime import timedelta
import os

from backend.app.errors import AppError
from backend.app.db.crud import (
    UserForm,
    check_user,
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user,
)


def signup_user(user_regis_data: dict):
    existing_user = check_user(user_regis_data["account"])

    if existing_user:
        raise AppError(400, "電子郵件重複")

    password_hs256 = get_password_hash(user_regis_data["password"])

    user_data = UserForm(
        user_regis_data["account"],
        password_hs256,
        user_regis_data["name"],
        user_regis_data["position"],
    )

    user_data.insert_user()

    return {"ok": True}


async def authenticate_user(user_data: dict):
    existing_user = check_user(user_data.get("account"))
    print(existing_user)

    if not existing_user:
        raise AppError(400, "查無使用者或密碼錯誤")

    if not verify_password(user_data["password"], existing_user["password"]):
        raise AppError(400, "查無使用者或密碼錯誤")

    access_token_expires = timedelta(days=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")))
    access_token = create_access_token(
        data={
            "username": existing_user["name"],
            "account": existing_user["account"],
            "position": existing_user["position"],
            "user_id": existing_user["id"],
        },
        expires_delta=access_token_expires,
    )

    return {"token": access_token}


async def get_current_user_profile(request: Request):
    current_user = await get_current_active_user(request)
    if not current_user:
        return {"data": None}

    return {
        "data": {
            "id": current_user["id"],
            "name": current_user["name"],
            "account": current_user["account"],
            "position": current_user["position"],
        }
    }
