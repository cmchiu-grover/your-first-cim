from fastapi import APIRouter, Query, Response
from fastapi.responses import StreamingResponse
from typing import Optional
import io
from backend.app.services import queries_service

router = APIRouter()

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
    return await queries_service.query_standard_times_list(
        prod_code, prod_name, eqp_type, station_name, module_name, creation_time, page
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
    csv_content, filename = await queries_service.download_standard_times_csv(
        prod_code, prod_name, eqp_type, station_name, module_name, creation_time
    )

    if csv_content is None:
        return Response(content="No data found for the given criteria.", media_type="text/plain")

    return StreamingResponse(
        io.BytesIO(csv_content.encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/api/eqp_status_query/ie")
async def query_eqp_status_ie(
    work_date: Optional[str] = Query(None, description="產品代碼"),
    module_name: Optional[str] = Query(None, description="模組名稱"),
    station_name: Optional[str] = Query(None, description="站點名稱"),
    eqp_type: Optional[str] = Query(None, description="設備類型"),
    eqp_code: Optional[str] = Query(None, description="設備號碼"),
    page: int = Query(1, ge=1, description="頁碼")
):
    return await queries_service.query_eqp_status_ie(
        work_date, module_name, station_name, eqp_type, eqp_code, page
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
    return await queries_service.query_eqp_status_eq(
        work_date, module_name, station_name, eqp_type, eqp_code, page
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
    return await queries_service.query_eqp_status_mfg(
        work_date, module_name, station_name, eqp_type, eqp_code, page
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
    return await queries_service.query_eqp_wip_list(
        work_date, module_name, station_name, eqp_type, eqp_code, page
    )
