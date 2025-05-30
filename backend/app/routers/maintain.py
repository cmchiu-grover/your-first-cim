from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from backend.app.db.crud import update_standard_time_value,get_current_active_user, create_notification_and_assign_users, StandardTimeUpdate
from backend.app.db.dbquery import get_all_user_ids
from backend.app.models.redis_pubsub import publish_update
from backend.app.models.notification import NotificationCreate
from typing import List
import csv
import io

router = APIRouter()

@router.put("/api/ie_maintain_stdt")
async def update_standard_times(data: List[StandardTimeUpdate], request: Request,):
    current_user = await get_current_active_user(request)
    print(f"當前使用者: {current_user.get("name")}")
    print(f"接收到的更新資料: {data}")
    updated_count = 0
    for row in data:
        try:
            if update_standard_time_value(row):
                updated_count += 1
            else:
                return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"更新失敗，找不到符合條件的資料..."
                    }
                    )

        except Exception as e:
            print(f"更新失敗: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "error":True,
                    "message":"伺服器錯誤..."
                    }
                    )
        
    notif = NotificationCreate(
        title="標準工時更新",
        message=f"{current_user.get("name")} 更新了 {updated_count} 筆標準工時資料。",
        event_type="standard_time_updated"
    )

    user_ids = get_all_user_ids()  
    create_notification_and_assign_users(notif, user_ids)

    await publish_update(notif.message)

    return {
        "ok": True,
        "message": f"成功更新 {updated_count} 筆資料。"
    }

@router.put("/api/ie_maintain_stdt/upload_csv")
async def upload_csv_file(request: Request, file: UploadFile = File(...),):
    current_user = await get_current_active_user(request)
    print(f"當前使用者: {current_user.get("name")}")
    print(f"接收到的更新資料: {file}")

    if not file.filename.endswith(".csv"):
        return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"只支援 CSV 檔案。"
                    }
                    )

    contents = await file.read()
    decoded = contents.decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(decoded))

    updated = 0
    failed_rows = []

    for idx, row in enumerate(csv_reader, start=1):
        try:
            data = {
                "prod_code": row["prod_code"],
                "eqp_type": row["eqp_type"],
                "station_name": row["station_name"],
                "stdt": float(row["standard_time_value"]),
            }
            success = update_standard_time_value(data)
            if success:
                updated += 1
            else:
                failed_rows.append(idx)
        except Exception as e:
            print(f"第 {idx} 列處理失敗：{e}")
            failed_rows.append(idx)
    
    notif = NotificationCreate(
        title="標準工時更新",
        message=f"{current_user.get("name")} 更新了 {updated} 筆標準工時資料。",
        event_type="standard_time_updated"
    )

    user_ids = get_all_user_ids()  
    create_notification_and_assign_users(notif, user_ids)

    await publish_update(notif.message)

    return JSONResponse(
            status_code=200,
            content={
                "ok": True,
                "message": f"成功更新 {updated} 筆資料。失敗 {len(failed_rows)} 筆。",
                }
                )
