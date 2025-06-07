from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse, StreamingResponse
# from backend.app.models.plot import create_eq_gantt_chart
# from backend.app.db.dbquery import get_gantt_chart_data
from datetime import datetime
from datetime import timedelta
# from pydantic import BaseModel
# from typing import Optional

router = APIRouter()

@router.get("/api/oee/yesterday")
async def get_gantt_chart_url(
    request: Request,
):
    try:
        now = datetime.now()

        if now.hour < 7:
            target_date = now - timedelta(days=2)
        else:
            target_date = now - timedelta(days=1)

        formatted_date = target_date.strftime("%Y/%m/%d")
        yesterday_oee_data = get_yesterday_oee_data(
            work_date=formatted_date,
        )

        print(yesterday_oee_data)

        return JSONResponse(
            status_code=200,
            content={
                "ok":True,
                "data":[
                {
                    "module": station["module_name"],
                    "station": station["station_name"],
                    "avil_rate": station["avil_rate"],
                }
                for station in yesterday_oee_data
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

