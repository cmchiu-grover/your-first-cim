from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from backend.app.db.dbquery import query_standard_times, query_all_standard_times, query_eq_status_eq, query_eq_status_mfg, query_eqp_code_wip
from typing import List, Optional
import csv 
import io 


router = APIRouter()


class StandardTimeRecord(BaseModel):
    standard_time_id: int
    prod_code: str
    prod_name: str
    eqp_type: str
    module_name: str
    station_name: str
    standard_time_value: float
    standard_time_description: Optional[str] = None
    creation_time: datetime
    updated_time: datetime

class StandardTimeQueryResult(BaseModel):
    results: List[StandardTimeRecord]
    total_pages: int
    current_page: int
    total_records: int

@router.get("/api/standard_times_query")
async def query_standard_time(
    prod_code: Optional[str] = Query(None, description="產品代碼"),
    prod_name: Optional[str] = Query(None, description="產品名稱"),
    eqp_type: Optional[str] = Query(None, description="設備類型名稱"),
    station_name: Optional[str] = Query(None, description="站點名稱"),
    module_name: Optional[str] = Query(None, description="模組名稱"),
    creation_time: Optional[str] = Query(None, description="創建時間 (YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS)"),
    page: int = Query(1, ge=1, description="頁碼")
):
    try:
        data_list = query_standard_times(
            prod_code=prod_code,
            prod_name=prod_name,
            eqp_type=eqp_type,
            station_name=station_name,
            module_name=module_name,
            creation_time=creation_time,
            page=page
        )

        total_pages = data_list[0]
        next_page = data_list[1]
        results = data_list[2]

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

    except Exception as e:
        print(f"query_standard_times 錯誤：{e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

@router.get("/api/standard_times_download_csv")
async def download_standard_time_csv(
    prod_code: Optional[str] = Query(None, description="產品代碼"),
    prod_name: Optional[str] = Query(None, description="產品名稱"),
    eqp_type: Optional[str] = Query(None, description="設備類型名稱"),
    station_name: Optional[str] = Query(None, description="站點名稱"),
    module_name: Optional[str] = Query(None, description="模組名稱"),
    creation_time: Optional[str] = Query(None, description="創建時間 (YYYY-MM-DD)"),
):

    try:
        records = query_all_standard_times(
            prod_code=prod_code,
            prod_name=prod_name,
            eqp_type=eqp_type,
            station_name=station_name,
            module_name=module_name,
            creation_time=creation_time,
        )

        if not records:
            return Response(content="No data found for the given criteria.", media_type="text/plain")
            
        output = io.StringIO()
        
        fieldnames = list(records[0].keys()) 
        

        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader() 
        writer.writerows(records) 

        csv_content = output.getvalue()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"standard_times_query_results_{timestamp}.csv"

        return StreamingResponse(
            io.BytesIO(csv_content.encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        print(f"下載 CSV 時發生錯誤: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

@router.get("/api/eqp_status_query/eq")
async def query_eqp_status_eq(
    work_date: Optional[str] = Query(None, description="產品代碼"),
    module_name: Optional[str] = Query(None, description="模組名稱"),
    station_name: Optional[str] = Query(None, description="站點名稱"),
    eqp_type: Optional[str] = Query(None, description="設備類型"),
    eqp_code: Optional[str] = Query(None, description="設備號碼"),
    page: int = Query(1, ge=1, description="頁碼")
):
    try:
        data_list = query_eq_status_eq(
            work_date=work_date,
            module_name=module_name,
            station_name=station_name,
            eqp_type=eqp_type,
            eqp_code=eqp_code,
            page=page
        )

        total_pages = data_list[0]
        next_page = data_list[1]
        results = data_list[2]

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

    except Exception as e:
        print(f"query_eq_status_eq 錯誤：{e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

@router.get("/api/eqp_status_query/mfg")
async def query_eqp_status_mfg(
    work_date: Optional[str] = Query(None, description="產品代碼"),
    module_name: Optional[str] = Query(None, description="模組名稱"),
    station_name: Optional[str] = Query(None, description="站點名稱"),
    eqp_type: Optional[str] = Query(None, description="設備類型"),
    eqp_code: Optional[str] = Query(None, description="設備號碼"),
    page: int = Query(1, ge=1, description="頁碼")
):
    try:
        data_list = query_eq_status_mfg(
            work_date=work_date,
            module_name=module_name,
            station_name=station_name,
            eqp_type=eqp_type,
            eqp_code=eqp_code,
            page=page
        )

        total_pages = data_list[0]
        next_page = data_list[1]
        results = data_list[2]

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

    except Exception as e:
        print(f"query_eq_status_eq 錯誤：{e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

@router.get("/api/wip_query")
async def query_eqp_wip(
    work_date: Optional[str] = Query(None, description="產品代碼"),
    module_name: Optional[str] = Query(None, description="模組名稱"),
    station_name: Optional[str] = Query(None, description="站點名稱"),
    eqp_type: Optional[str] = Query(None, description="設備類型"),
    eqp_code: Optional[str] = Query(None, description="設備號碼"),
    page: int = Query(1, ge=1, description="頁碼")
):
    try:
        data_list = query_eqp_code_wip(
            work_date=work_date,
            module_name=module_name,
            station_name=station_name,
            eqp_type=eqp_type,
            eqp_code=eqp_code,
            page=page
        )

        total_pages = data_list[0]
        next_page = data_list[1]
        results = data_list[2]

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
                    "prod_code": item["prod_code"],
                    "wip_qty": item["wip_qty"],

                }
                for item in results
            ]
        }

    except Exception as e:
        print(f"query_eqp_wip 錯誤：{e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )
