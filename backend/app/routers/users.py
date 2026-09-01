from fastapi import APIRouter, Body, Request
from backend.app.services import users_service

router = APIRouter()

@router.post("/api/user")
def signup(user_regis_data: dict = Body(...)):
    return users_service.signup_user(user_regis_data)

@router.put("/api/user/auth")
async def signin_form(user_data: dict = Body(...)):
    return await users_service.authenticate_user(user_data)

@router.get("/api/user/auth")
async def get_user_data(request: Request):
    return await users_service.get_current_user_profile(request)
