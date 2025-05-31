from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from backend.app.models.plot import create_eq_gantt_chart
from datetime import datetime
from datetime import timedelta

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