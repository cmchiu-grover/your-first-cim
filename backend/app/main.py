from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers.first_wk import router as first_week_router

app = FastAPI()

# app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(first_week_router)

# @app.get("/msg_img_posts", include_in_schema=False)
# async def index(request: Request):
#     return FileResponse("frontend/static/msg_img_posts.html", media_type="text/html")