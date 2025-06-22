from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse, StreamingResponse
from backend.app.db.dbquery import get_yesterday_oee_data, get_oee_data, get_station_oee_data
from typing import Optional
from datetime import datetime
from datetime import timedelta

router = APIRouter()

@router.get("/api/oee")
async def api_get_oee_data(
    request: Request,
    work_date: Optional[str] = Query(None, description="work_date (YYYY-MM-DD)"),
    date: Optional[str] = Query(None, description="Shortcut for date like 'yesterday'")
):
    try:
        if date == "yesterday":
            formatted_date = datetime.today().date() - timedelta(days=1)
        elif work_date:
            formatted_date = datetime.strptime(work_date, "%Y-%m-%d").date()
        else:
            formatted_date = datetime.today().date()

        oee_data = get_oee_data(formatted_date)
        print(oee_data)

        return JSONResponse(
            status_code=200,
            content={
                "ok":True,
                "date": formatted_date.isoformat(),
                "data":[
                {
                    "metrics": item["Metrics"],
                    "oee_rate": float(item["oee_rate"]),
                    "avail_rate": float(item["avail_rate"]),
                    "perf_rate": float(item["perf_rate"]),
                }
                for item in oee_data
                ]
                }
                )

    except Exception as e:
        print(f"query_standard_times 錯誤：{e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

@router.get("/api/oee/stations")
async def api_get_station_oee_data(
    request: Request,
    station_name: Optional[str] = Query(None, description="station_name"),
    work_date: Optional[str] = Query(None, description="work_date (YYYY-MM-DD)")
):
    try:
        formatted_date = datetime.strptime(work_date, "%Y-%m-%d").date()

        station_oee_data = get_station_oee_data(station_name, formatted_date)
        print(station_oee_data)

        return JSONResponse(
            status_code=200,
            content={
                "ok":True,
                "data":[
                {
                    "metrics": item["Metrics"],
                    "oee_rate": float(item["oee_rate"]),
                    "avail_rate": float(item["avail_rate"]),
                    "perf_rate": float(item["perf_rate"]),
                }
                for item in station_oee_data
                ]
                }
                )

    except Exception as e:
        print(f"query_standard_times 錯誤：{e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

