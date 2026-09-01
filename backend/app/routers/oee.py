from fastapi import APIRouter, Request, Query
from typing import Optional
from backend.app.services import oee_service

router = APIRouter()

@router.get("/api/oee")
async def api_get_oee_data(
    request: Request,
    work_date: Optional[str] = Query(None, description="work_date (YYYY-MM-DD)"),
    date: Optional[str] = Query(None, description="Shortcut for date like 'yesterday'")
):
    return await oee_service.get_oee(work_date, date)

@router.get("/api/oee/stations")
async def api_get_station_oee_data(
    request: Request,
    station_name: Optional[str] = Query(None, description="station_name"),
    work_date: Optional[str] = Query(None, description="work_date (YYYY-MM-DD)")
):
    return await oee_service.get_station_oee(station_name, work_date)
