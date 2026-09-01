from datetime import datetime
from typing import Optional
import csv
import io

from backend.app.db.dbquery import (
    query_standard_times,
    query_all_standard_times,
    query_eq_status_eq,
    query_eq_status_mfg,
    query_eqp_code_wip,
    query_eq_status_ie,
)


async def query_standard_times_list(
    prod_code: Optional[str],
    prod_name: Optional[str],
    eqp_type: Optional[str],
    station_name: Optional[str],
    module_name: Optional[str],
    creation_time: Optional[str],
    page: int,
):
    total_pages, next_page, results = query_standard_times(
        prod_code=prod_code,
        prod_name=prod_name,
        eqp_type=eqp_type,
        station_name=station_name,
        module_name=module_name,
        creation_time=creation_time,
        page=page,
    )

    return {
        "totalPages": total_pages,
        "nextPage": next_page,
        "data": [
            {
                "standard_time_id": item["standard_time_id"],
                "prod_code": item["prod_code"],
                "prod_name": item["prod_name"],
                "eqp_type": item["eqp_type"],
                "module_name": item["module_name"],
                "station_name": item["station_name"],
                "stdt": float(item["standard_time_value"]),
                "updated_time": item["updated_time"].strftime('%Y-%m-%d %H:%M:%S'),
                "description": item.get("standard_time_description", ""),
            }
            for item in results
        ]
    }


async def download_standard_times_csv(
    prod_code: Optional[str],
    prod_name: Optional[str],
    eqp_type: Optional[str],
    station_name: Optional[str],
    module_name: Optional[str],
    creation_time: Optional[str],
):
    records = query_all_standard_times(
        prod_code=prod_code,
        prod_name=prod_name,
        eqp_type=eqp_type,
        station_name=station_name,
        module_name=module_name,
        creation_time=creation_time,
    )

    if not records:
        return None, None

    output = io.StringIO()
    fieldnames = list(records[0].keys())

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

    csv_content = output.getvalue()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"standard_times_query_results_{timestamp}.csv"

    return csv_content, filename


def _serialize_eqp_status_page(data_list):
    total_pages, next_page, results = data_list

    return {
        "totalPages": total_pages,
        "nextPage": next_page,
        "data": [
            {
                "id": item["event_id"],
                "work_date": item["work_date"].strftime('%Y-%m-%d'),
                "module_name": item["module_name"],
                "station_name": item["station_name"],
                "eqp_type": item["eqp_type"],
                "eqp_code": item["eqp_code"],
                "start_time": item["start_time"].strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": item["end_time"].strftime('%Y-%m-%d %H:%M:%S'),
                "duration": float(item["duration"]),
                "status": item["status_name"],
                "comment": item.get("comment", ""),
            }
            for item in results
        ]
    }


async def query_eqp_status_ie(
    work_date: Optional[str],
    module_name: Optional[str],
    station_name: Optional[str],
    eqp_type: Optional[str],
    eqp_code: Optional[str],
    page: int,
):
    data_list = query_eq_status_ie(
        work_date=work_date,
        module_name=module_name,
        station_name=station_name,
        eqp_type=eqp_type,
        eqp_code=eqp_code,
        page=page,
    )
    return _serialize_eqp_status_page(data_list)


async def query_eqp_status_eq(
    work_date: Optional[str],
    module_name: Optional[str],
    station_name: Optional[str],
    eqp_type: Optional[str],
    eqp_code: Optional[str],
    page: int,
):
    data_list = query_eq_status_eq(
        work_date=work_date,
        module_name=module_name,
        station_name=station_name,
        eqp_type=eqp_type,
        eqp_code=eqp_code,
        page=page,
    )
    return _serialize_eqp_status_page(data_list)


async def query_eqp_status_mfg(
    work_date: Optional[str],
    module_name: Optional[str],
    station_name: Optional[str],
    eqp_type: Optional[str],
    eqp_code: Optional[str],
    page: int,
):
    data_list = query_eq_status_mfg(
        work_date=work_date,
        module_name=module_name,
        station_name=station_name,
        eqp_type=eqp_type,
        eqp_code=eqp_code,
        page=page,
    )
    return _serialize_eqp_status_page(data_list)


async def query_eqp_wip_list(
    work_date: Optional[str],
    module_name: Optional[str],
    station_name: Optional[str],
    eqp_type: Optional[str],
    eqp_code: Optional[str],
    page: int,
):
    total_pages, next_page, results = query_eqp_code_wip(
        work_date=work_date,
        module_name=module_name,
        station_name=station_name,
        eqp_type=eqp_type,
        eqp_code=eqp_code,
        page=page,
    )

    return {
        "totalPages": total_pages,
        "nextPage": next_page,
        "data": [
            {
                "id": item["id"],
                "work_date": item["work_date"].strftime('%Y-%m-%d'),
                "module_name": item["module_name"],
                "station_name": item["station_name"],
                "eqp_type": item["eqp_type"],
                "eqp_code": item["eqp_code"],
                "prod_code": item["prod_code"],
                "wip_qty": item["wip_qty"],
            }
            for item in results
        ]
    }
