from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from backend.app.db.dbquery import get_temp_oee_data
from backend.app.db.crud import insert_final_oee_data, delete_temp_oee_data

def process_oee_data():
    print("開始移動 OEE 資料")
    tz = ZoneInfo("Asia/Taipei")

    today = datetime.now(tz).date()
    target_day = today - timedelta(days=4)
    temp_oee_data = get_temp_oee_data(target_day)

    insert_final_oee_data(temp_oee_data)
    delete_temp_oee_data(temp_oee_data)