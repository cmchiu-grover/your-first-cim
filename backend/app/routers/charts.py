from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from backend.app.models.plot import create_eq_gantt_chart


router = APIRouter()

@router.get("/api/chart/eqganttchart")
def eq_gantt_chart():
    
    try:
        eq_gantt_chart_img = create_eq_gantt_chart()

        return StreamingResponse(eq_gantt_chart_img, media_type="image/png")

    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            status_code=500,
            content={"error": True,
                     "message":"無法製圖！"}
                     )