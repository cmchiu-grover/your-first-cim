from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.app.routers.charts import router as eqganttchart_router
from backend.app.routers.users import router as user_router
from backend.app.routers.queries import router as query_router
from backend.app.routers.maintain import router as maintain_router
from backend.app.routers.sse import router as sse_router
from backend.app.routers.notifications import router as notifications_router


# from app.routers.first_wk import router as first_week_router
import redis.asyncio as redis

app = FastAPI()

app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(eqganttchart_router)
app.include_router(user_router)
app.include_router(query_router)
app.include_router(maintain_router)
app.include_router(sse_router)
app.include_router(notifications_router)

@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("frontend/static/index.html", media_type="text/html")

@app.get("/dashboard", include_in_schema=False)
async def index(request: Request):
    return FileResponse("frontend/static/dashboard.html", media_type="text/html")

@app.get("/iemaintain", include_in_schema=False)
async def iemaintain(request: Request):
    return FileResponse("frontend/static/iemaintain.html", media_type="text/html")

@app.get("/iequery", include_in_schema=False)
async def iemaintain(request: Request):
    return FileResponse("frontend/static/iequery.html", media_type="text/html")

@app.get("/eqganttchart", include_in_schema=False)
async def eqganttchart(request: Request):
    return FileResponse("frontend/static/eqganttchart.html", media_type="text/html")

@app.get("/notifications", include_in_schema=False)
async def template(request: Request):
    return FileResponse("frontend/static/notifications.html", media_type="text/html")

@app.get("/template", include_in_schema=False)
async def template(request: Request):
    return FileResponse("frontend/static/template.html", media_type="text/html")

