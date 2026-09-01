from datetime import datetime
from typing import Optional

from backend.app.db.dbquery import get_yesterday_oee_data, get_oee_data, get_station_oee_data


def _serialize_oee_rows(rows):
    return [
        {
            "metrics": item["Metrics"],
            "oee_rate": float(item["oee_rate"]),
            "avail_rate": float(item["avail_rate"]),
            "perf_rate": float(item["perf_rate"]),
        }
        for item in rows
    ]


async def get_oee(work_date: Optional[str], date: Optional[str]):
    if date == "yesterday":
        oee_data = get_yesterday_oee_data()
        return {
            "ok": True,
            "date": oee_data[0],
            "data": _serialize_oee_rows(oee_data[1]),
        }

    if work_date:
        formatted_date = datetime.strptime(work_date, "%Y-%m-%d").date()
    else:
        formatted_date = datetime.today().date()

    oee_data = get_oee_data(formatted_date)
    print(oee_data)

    return {
        "ok": True,
        "date": formatted_date.isoformat(),
        "data": _serialize_oee_rows(oee_data),
    }


async def get_station_oee(station_name: Optional[str], work_date: Optional[str]):
    formatted_date = datetime.strptime(work_date, "%Y-%m-%d").date()

    station_oee_data = get_station_oee_data(station_name, formatted_date)
    print(station_oee_data)

    return {
        "ok": True,
        "data": _serialize_oee_rows(station_oee_data),
    }
