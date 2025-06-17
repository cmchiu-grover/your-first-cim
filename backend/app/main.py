from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Routers
from backend.app.routers.charts import router as eqganttchart_router
from backend.app.routers.users import router as user_router
from backend.app.routers.queries import router as query_router
from backend.app.routers.maintain import router as maintain_router
from backend.app.routers.sse import router as sse_router
from backend.app.routers.notifications import router as notifications_router
from backend.app.routers.oee import router as oee_router

# APScheduler
from backend.app.routers.daily_jobs import start_daily_jobs, scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("APScheduler 啟動")
    start_daily_jobs()  # 啟動所有排程
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


app.include_router(eqganttchart_router)
app.include_router(user_router)
app.include_router(query_router)
app.include_router(maintain_router)
app.include_router(sse_router)
app.include_router(notifications_router)
app.include_router(oee_router)

@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("frontend/static/index.html", media_type="text/html")

@app.get("/dashboard", include_in_schema=False)
async def dashboard(request: Request):
    return FileResponse("frontend/static/dashboard.html", media_type="text/html")

@app.get("/iemaintain", include_in_schema=False)
async def iemaintain(request: Request):
    return FileResponse("frontend/static/iemaintain.html", media_type="text/html")

@app.get("/iequery", include_in_schema=False)
async def iequery(request: Request):
    return FileResponse("frontend/static/iequery.html", media_type="text/html")

@app.get("/eqganttchart", include_in_schema=False)
async def eqganttchart(request: Request):
    return FileResponse("frontend/static/eqganttchart.html", media_type="text/html")

@app.get("/notifications", include_in_schema=False)
async def notifications(request: Request):
    return FileResponse("frontend/static/notifications.html", media_type="text/html")

@app.get("/oee", include_in_schema=False)
async def oee(request: Request):
    return FileResponse("frontend/static/oee.html", media_type="text/html")

@app.get("/eqmaintain", include_in_schema=False)
async def eqmaintain(request: Request):
    return FileResponse("frontend/static/eqmaintain.html", media_type="text/html")

@app.get("/mfgmaintain", include_in_schema=False)
async def mfgmaintain(request: Request):
    return FileResponse("frontend/static/mfgmaintain.html", media_type="text/html")

@app.get("/wipquery", include_in_schema=False)
async def mfgmaintain(request: Request):
    return FileResponse("frontend/static/wipquery.html", media_type="text/html")

@app.get("/template", include_in_schema=False)
async def template(request: Request):
    return FileResponse("frontend/static/template.html", media_type="text/html")
