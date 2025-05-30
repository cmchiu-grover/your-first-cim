from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from backend.app.db.crud import UserForm, check_user, get_password_hash, verify_password, create_access_token, get_current_active_user
from datetime import timedelta
from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter()

@router.post("/api/user")
def signup(user_regis_data: dict = Body(...)):
    try:
        existing_user = check_user(user_regis_data["account"])

        if existing_user: 
            return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"電子郵件重複"
                    }
                    )
        
        password_hs256 = get_password_hash(user_regis_data["password"])
        
        user_data = UserForm(user_regis_data["account"], password_hs256, user_regis_data["name"], user_regis_data["position"])

        user_data.insert_user()

        return JSONResponse(
            status_code=200,
            content={
                "ok": True
                }
                )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )  

@router.put("/api/user/auth")
async def signin_form(user_data: dict = Body(...)):
    try:
        
        existing_user = check_user(user_data.get("account"))
        print(existing_user)

        if not existing_user:
            return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"查無使用者或密碼錯誤"
                    }
                    )
        
        
        if verify_password(user_data["password"], existing_user["password"]):
            access_token_expires = timedelta(days = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")))
            access_token = create_access_token(
                data={
                    "username": existing_user["name"],
                    "account": existing_user["account"],
                    "position": existing_user["position"],
                    "user_id":existing_user["id"]
                    },
                    expires_delta = access_token_expires
                    )

            return JSONResponse(
                status_code=200,
                content={
                    "token": access_token
                    },
                    )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"查無使用者或密碼錯誤"
                    }
                    )
        
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

@router.get("/api/user/auth")
async def get_user_data(request: Request):
    current_user = await get_current_active_user(request)
    if not current_user:
        return JSONResponse(
            status_code=200,
            content = { "data": None
                }
                )

    return JSONResponse(
            status_code=200,
            content = { "data": {
                "id": current_user["id"],
                "name": current_user["name"],
                "account": current_user["account"],
                "position": current_user["position"]
                }
                }
                )
