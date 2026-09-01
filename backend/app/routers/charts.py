from fastapi import APIRouter, Request, Query
from fastapi.responses import StreamingResponse
from typing import Optional
from backend.app.services import charts_service

router = APIRouter()

@router.get("/api/chart/eqganttchart")
def eq_gantt_chart():
    eq_gantt_chart_img = charts_service.render_eq_gantt_chart()
    return StreamingResponse(eq_gantt_chart_img, media_type="image/png")

@router.get("/api/chart/ganttchart/yesterday")
async def get_yesterday_gantt_chart_url(
    request: Request,
):
    return await charts_service.get_yesterday_gantt_chart_url()

@router.get("/api/chart/ganttchart")
async def get_gantt_chart_url(
    request: Request,
    station_name: Optional[str] = Query(None, description="station_name"),
    work_date: Optional[str] = Query(None, description="work_date (YYYY-MM-DD)")
):
    return await charts_service.get_gantt_chart_url(station_name, work_date)
