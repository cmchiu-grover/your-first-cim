from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from backend.app.db.crud import update_standard_time_value,get_current_active_user, create_notification_and_assign_users, StandardTimeUpdate, EqpStatusUpdate, update_eqp_status_comment
from backend.app.db.dbquery import get_all_user_ids, query_eqp_data
from backend.app.models.redis_pubsub import publish_update
from backend.app.models.notification import NotificationCreate
from backend.app.models.update_temp_oee import update_temp_oee_after_updating_stdt
from typing import List
import csv
import io

router = APIRouter()

@router.put("/api/ie_maintain_stdt")
async def update_standard_times(data: List[dict], request: Request,):
    try:
        current_user = await get_current_active_user(request)
        if not current_user:
            return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"權限不足，請先登入。"
                    }
                    )
        
        elif current_user.get("position") != "IE":
            return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"權限不足，並非 IE 同仁。"
                    }
                    )

        updated_count = 0
        affected_eqp_ids = set()
        affected_details = []
        for row in data:
            eqp_list = []
            if update_standard_time_value(row):
                eqp_type = row.get("eqp_type")
                eqp_data = query_eqp_data(eqp_type)
                for eqp in eqp_data:
                    eqp_list.append(eqp.get("id"))
                print(f"eqp_list: {eqp_list}")
                temp_result_list = update_temp_oee_after_updating_stdt(eqp_list)
                print(f"temp_result_list: {temp_result_list}")
                if not temp_result_list:
                    updated_count += 1
                    continue

                for item in temp_result_list:
                    affected_eqp_ids.add(item.get("eqp_id"))
                
                updated_count += 1

            else:
                return JSONResponse(
                status_code=400,
                content={
                    "error":True,
                    "message":"更新失敗，找不到符合條件的資料..."
                    }
                    )
        
        details_text = ""
        print(f"affected_details: {affected_details}")
        for item in affected_details:
            eqp_code = item["eqp_code"]
            date = item["work_date"].strftime("%Y-%m-%d")
            asis_oee = item["asis_oee_rate"]
            tobe_oee = item["tobe_oee_rate"]
            asis_perf = item["asis_perf_rate"]
            tobe_perf = item["tobe_perf_rate"]
            if asis_oee == tobe_oee and asis_perf == tobe_perf:
                continue
            details_text += f"- {eqp_code}({date})：OEE {asis_oee} → {tobe_oee}，作業效率 {asis_perf} → {tobe_perf}\n"

        
        notif = NotificationCreate(
            title="標準工時更新",
            message=(
                f"{current_user.get('name')} 更新了 {updated_count} 筆標準工時資料，"
                f"影響機台 {len(affected_eqp_ids)} 台 OEE 資料：\n\n{details_text.strip()}"
            ),
            event_type="standard_time_updated"
        )

        user_ids = get_all_user_ids()  
        create_notification_and_assign_users(notif, user_ids)

        await publish_update(notif.message)

        return {
            "ok": True,
            "message": f"成功更新 {updated_count} 筆資料。"
        }
    
    except Exception as e:
        print(f"更新失敗: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )

@router.put("/api/ie_maintain_stdt/upload_csv")
async def upload_csv_file(request: Request, file: UploadFile = File(...),):
    current_user = await get_current_active_user(request)
    if not current_user:
        return JSONResponse(
            status_code=400,
            content={
                "error":True,
                "message":"權限不足，請先登入。"
                }
                )
    
    elif current_user.get("position") != "IE":
        return JSONResponse(
            status_code=400,
            content={
                "error":True,
                "message":"權限不足，並非 IE 同仁。"
                }
                )


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
    affected_eqp_ids = set()
    affected_details = []

    for idx, row in enumerate(csv_reader, start=1):
        eqp_list = []
        try:
            data = {
                "prod_code": row["prod_code"],
                "eqp_type": row["eqp_type"],
                "station_name": row["station_name"],
                "stdt": float(row["standard_time_value"]),
            }
            success = update_standard_time_value(data)
            if success:
                eqp_type = data.get("eqp_type")
                eqp_data = query_eqp_data(eqp_type)
                for eqp in eqp_data:
                    eqp_list.append(eqp.get("id"))
                temp_result_list = update_temp_oee_after_updating_stdt(eqp_list)
                for item in temp_result_list:
                    affected_eqp_ids.add(item.get("eqp_id"))
                    affected_details.append(item)
                updated += 1
                
            else:
                failed_rows.append(idx)
        except Exception as e:
            print(f"第 {idx} 列處理失敗：{e}")
            failed_rows.append(idx)
    
    details_text = ""
    for item in affected_details:
        eqp_code = item["eqp_code"]
        date = item["work_date"].strftime("%Y-%m-%d")
        asis_oee = item["asis_oee_rate"]
        tobe_oee = item["tobe_oee_rate"]
        asis_perf = item["asis_perf_rate"]
        tobe_perf = item["tobe_perf_rate"]
        if asis_oee == tobe_oee and asis_perf == tobe_perf:
            continue
        details_text += f"- {eqp_code}({date})：OEE {asis_oee} → {tobe_oee}，作業效率 {asis_perf} → {tobe_perf}\n"

    notif = NotificationCreate(
        title="標準工時更新",
        message=(
            f"{current_user.get('name')} 更新了 {updated} 筆標準工時資料，"
            f"影響機台 {len(affected_eqp_ids)} 台 OEE 資料：\n\n{details_text.strip()}"
        ),
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

@router.put("/api/eqp_status_update")
async def update_standard_times(data: List[EqpStatusUpdate], request: Request,):
    current_user = await get_current_active_user(request)
    print(f"當前使用者: {current_user.get("name")}")
    print(f"接收到的更新資料: {data}")
    updated_count = 0
    for row in data:
        try:
            if update_eqp_status_comment(row):
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
        title="機況 comment 更新",
        message=f"{current_user.get("name")} 更新了 {updated_count} 筆機況 comment。",
        event_type="eqp_status_updated"
    )

    user_ids = get_all_user_ids()  
    create_notification_and_assign_users(notif, user_ids)

    await publish_update(notif.message)

    return {
        "ok": True,
        "message": f"成功更新 {updated_count} 筆資料。"
    }
