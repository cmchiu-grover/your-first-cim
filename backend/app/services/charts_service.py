from datetime import datetime, timedelta, date, time
from typing import Optional
from zoneinfo import ZoneInfo

from backend.app.errors import AppError
from backend.app.models.plot import create_eq_gantt_chart
from backend.app.db.dbquery import get_gantt_chart_data

tz = ZoneInfo("Asia/Taipei")


def render_eq_gantt_chart():
    month_num = 4
    day_num = 30

    start_datetime_window = datetime(2025, month_num, day_num, 7, 0, 0)
    end_datetime_window = datetime(2025, month_num, day_num, 7, 0, 0) + timedelta(days=1)

    try:
        return create_eq_gantt_chart("CPU", start_datetime_window, end_datetime_window)
    except Exception as e:
        print("Error:", e)
        raise AppError(500, "無法製圖！")


async def get_yesterday_gantt_chart_url():
    now = datetime.now(tz)
    seven_am_today = datetime.combine(date.today(), time(7, 0)).replace(tzinfo=tz)

    if now < seven_am_today:
        yesterday_work_date = date.today() - timedelta(days=2)
    else:
        yesterday_work_date = date.today() - timedelta(days=1)

    data_list = get_gantt_chart_data(
        station_name="CPU",
        work_date=yesterday_work_date,
    )

    print(data_list)

    return {
        "ok": True,
        "url": data_list.get("image_url"),
    }


async def get_gantt_chart_url(station_name: Optional[str], work_date: Optional[str]):
    formatted_date = datetime.strptime(work_date, "%Y-%m-%d").strftime("%Y/%m/%d")
    data_list = get_gantt_chart_data(
        station_name=station_name,
        work_date=formatted_date,
    )

    print(data_list)

    return {
        "ok": True,
        "url": data_list.get("image_url"),
    }
