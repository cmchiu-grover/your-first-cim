from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from backend.app.models.generate_temp_oee import query_avail_rate, query_eqp_wip, query_stdt
from backend.app.db.crud import update_temp_oee_by_eqp_id
tz = ZoneInfo("Asia/Taipei")

def update_temp_oee_after_updating_stdt(eqp_list):
    today = datetime.now(tz).date()
    result_dict_list = []
    for day_i in range(1, 4):

        query_date = today - timedelta(days=day_i)

        for eqp_id in eqp_list:
            # 開始計算作業效率
            print(f"開始 query_avail_rate({eqp_id}, {query_date})")
            avail_rate_data = query_avail_rate(eqp_id, query_date)
            if not avail_rate_data:
                continue
            avail_rate = avail_rate_data.get("avail_rate")
            avail_mins = float(avail_rate) * 1440 / 100

            eqp_type_id = avail_rate_data.get("eqp_type_id")

            eqp_wip_data = query_eqp_wip(eqp_id, query_date) # 單一機台
            wip_operation_mins = 0

            for prod_id in eqp_wip_data:
                wip_operation_mins += query_stdt(prod_id.get("prod_id"), eqp_type_id) * prod_id.get("wip_qty")

            perf_rate = round(float(wip_operation_mins) / avail_mins * 100, 2)
            print(f"perf_rate: {perf_rate}")

            oee_rate = round(float(avail_rate) * perf_rate / 100 ,2)
            print(f"oee_rate: {oee_rate}")

            updated_dict = update_temp_oee_by_eqp_id(eqp_id, query_date, oee_rate, perf_rate)
            print(f"updated_dict: {updated_dict}")
            if updated_dict.get("asis_oee_rate") == updated_dict.get("tobe_oee_rate"):
                continue

            result_dict_list.append(updated_dict)
    print(f"result_dict_list: {result_dict_list}")
    return result_dict_list

