from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse, StreamingResponse
from backend.app.models.plot import create_eq_gantt_chart
from backend.app.db.dbquery import get_gantt_chart_data
from datetime import datetime, timedelta, date, time
from pydantic import BaseModel
from typing import Optional

router = APIRouter()



@router.get("/api/chart/eqganttchart")
def eq_gantt_chart():
    month_num = 4
    day_num = 30

    start_datetime_window = datetime(2025, month_num, day_num, 7, 0, 0)
    end_datetime_window = datetime(2025, month_num, day_num, 7, 0, 0)  + timedelta(days=1)
    
    try:
        eq_gantt_chart_img = create_eq_gantt_chart("CPU", start_datetime_window, end_datetime_window)

        return StreamingResponse(eq_gantt_chart_img, media_type="image/png")

    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            status_code=500,
            content={"error": True,
                     "message":"無法製圖！"}
                     )

class GanttChartRecord(BaseModel):
    station_name: str
    work_date: datetime

@router.get("/api/chart/ganttchart/yesterday")
async def get_gantt_chart_url(
    request: Request,
):
    try:
        now = datetime.now()
        seven_am_today = datetime.combine(date.today(), time(7, 0))

        if now < seven_am_today:
        
            yesterday_work_date = date.today() - timedelta(days=1)
        else:
        
            yesterday_work_date = date.today()

        data_list = get_gantt_chart_data(
            station_name="CPU",
            work_date=yesterday_work_date,
        )

        print(data_list)

        gantt_chart_url = data_list.get('image_url')

        return JSONResponse(
            status_code=200,
            content={
                "ok":True,
                "url":gantt_chart_url
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


@router.get("/api/chart/ganttchart")
async def get_gantt_chart_url(
    request: Request,
    station_name: Optional[str] = Query(None, description="station_name"),
    work_date: Optional[str] = Query(None, description="work_date (YYYY-MM-DD)")
):
    try:
        formatted_date = datetime.strptime(work_date, "%Y-%m-%d").strftime("%Y/%m/%d")
        data_list = get_gantt_chart_data(
            station_name=station_name,
            work_date=formatted_date,
        )

        print(data_list)

        gantt_chart_url = data_list.get('image_url')

        return JSONResponse(
            status_code=200,
            content={
                "ok":True,
                "url":gantt_chart_url
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
