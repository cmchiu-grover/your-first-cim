from fastapi import APIRouter, Request, UploadFile, File
from typing import List
from backend.app.services import maintain_service

router = APIRouter()

@router.put("/api/ie_maintain_stdt")
async def update_standard_times(data: List[dict], request: Request):
    return await maintain_service.update_standard_times_batch(data, request)

@router.put("/api/ie_maintain_stdt/upload_csv")
async def upload_csv_file(request: Request, file: UploadFile = File(...)):
    return await maintain_service.upload_standard_times_csv(request, file)

@router.put("/api/eqp_status_update")
async def update_eqp_status(data: List[dict], request: Request):
    return await maintain_service.update_eqp_status_comments(data, request)
