import datetime
import random
from datetime import timedelta, time, datetime, date
from backend.app.db.connect import get_connection_pool
from zoneinfo import ZoneInfo

def generate_insert_eqp_info_sql(eq_id, work_date, start_of_window, end_of_window, target_run_min_seconds, target_run_max_seconds):
    print(f"-- Data for eq_id: {eq_id}")

    # --- Step 1: 先隨機決定 target_run_seconds ---
    target_run_seconds = random.uniform(target_run_min_seconds, target_run_max_seconds)

    # --- Step 2: 再隨機決定 target_down_seconds（例如：3024~5616 秒）---
    target_down_seconds = random.uniform(3024, 5616)

    # --- Step 3: 剩下的時間為 target_idle_seconds ---
    total_seconds = (end_of_window - start_of_window).total_seconds()
    target_idle_seconds = total_seconds - target_run_seconds - target_down_seconds

    if target_idle_seconds < 0:
        print(f"-- Warning: target_idle_seconds is negative ({target_idle_seconds}). Adjusting target_down_seconds.")
        target_idle_seconds = 0
        target_down_seconds = total_seconds - target_run_seconds

    # --- Step 4: 建立時間區段 ---
    current_time = start_of_window
    slots = []

    while current_time < end_of_window:
        duration_seconds = random.randint(300, 5400)  # 每段 5 分鐘到 90 分鐘
        end = current_time + timedelta(seconds=duration_seconds)
        if end > end_of_window:
            end = end_of_window
        actual_duration = (end - current_time).total_seconds()
        if actual_duration > 0:
            slots.append({
                'start': current_time,
                'end': end,
                'duration': actual_duration
            })
        current_time = end

    # --- Step 5: 隨機打亂 slots ---
    random.shuffle(slots)

    # --- Step 6: 將狀態依照 target 數值分配 ---
    remaining_run = target_run_seconds
    remaining_down = target_down_seconds
    remaining_idle = target_idle_seconds

    for slot in slots:
        d = slot['duration']
        if remaining_run >= d:
            slot['status'] = 'run'
            remaining_run -= d
        elif remaining_down >= d:
            slot['status'] = 'down'
            remaining_down -= d
        else:
            slot['status'] = 'idle'
            remaining_idle -= d

    # --- Step 7: 依開始時間排序 slots ---
    slots.sort(key=lambda x: x['start'])

    # --- Step 8: 組成 INSERT SQL 語句 ---
    insert_statement = f"INSERT INTO eqp_status (eqp_id, work_date, start_time, end_time, hours, status_id) VALUES \n"
    values_list = []

    for slot in slots:
        work_date_str = work_date.strftime('%Y-%m-%d')
        start_time_str = slot['start'].strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = slot['end'].strftime('%Y-%m-%d %H:%M:%S')
        hour_time_value = slot['duration'] / 3600.0

        if slot['status'] == 'run':
            status_str = 1
        elif slot['status'] == 'down':
            status_str = 2
        elif slot['status'] == 'idle':
            status_str = 3
        else:
            status_str = 5  # unknown

        values_list.append(f"    ('{eq_id}', '{work_date_str}', '{start_time_str}', '{end_time_str}', {hour_time_value:.6f}, {status_str})")

    insert_statement += ",\n".join(values_list)
    insert_statement += ";\n"

    print("\n")
    return insert_statement

def generate_eqp_status():
    print("開始產生機況資料")
    eq_ids = [
    [2,0.983],
    [3,0.983],
    [4,0.983],
    [5,0.983],
    [6,0.983],
    [8,0.983],
    [9,0.5],
    [10,0.967],
    [11,0.967],
    [12,0.967],
    [13,0.3],
    [14,0.1],
    [15,0.97],
    [16,0.97],
    [17,0.97],
    [18,0.97],
    [19,0.97],
    [20,0.97],
    [21,0.97],
    [22,0.97],
    [23,0.97],
    [24,0.97],
    [25,0.93],
    [26,0.93],
    [27,0.93],
    [28,0.93],
    [29,0.93],
    [30,0.93],
    [31,0.93],
    [32,0.93],
    [33,0.93],
    [34,0.93],
    [35,0.9],
    [36,0.9],
    [37,0.983],
    [38,0.983],
    [39,0.983],
    [40,0.983],
    [41,0.983],
    [42,0.983],
    [43,0.983],
    [44,0.983],
    [45,0.983],
    [46,0.983],
    [47,0.983],
    [48,0.983],
    [49,0.983],
    [50,0.983],
    [51,0.983],
    [52,0.983],
    [53,0.983],
    [54,0.983],
    [55,0.985],
    [56,0.985],
    [57,0.985],
    [58,0.985],
    [59,0.985],
    [60,0.985],
    [61,0.985],
    [62,0.985],
    [63,0.985],
    [64,0.985],
    [65,0.985],
    [66,0.985],
    [67,0.985],
    [68,0.985],
    [69,0.985],
    [70,0.985],
    [71,0.985],
    [72,0.985],
    [73,0.985],
    [74,0.985],
    [75,0.985],
    [76,0.985],
    [77,0.985],
    [78,0.985],
    [79,0.985],
    [80,0.985],
    [81,0.997],
    [82,0.997],
    [83,0.997],
    [84,0.997],
    [85,0.997],
    [86,0.997],
    [87,0.997],
    [88,0.997],
    [89,0.997],
    [90,0.997],
    [91,0.997],
    [92,0.997],
    [93,0.997],
    [94,0.997],
    [95,0.997],
    [96,0.997],
    [97,0.997],
    [98,0.997],
    [99,0.997],
    [100,0.997],
    [101,0.997],
    [102,0.997],
    [103,0.997],
    [104,0.997],
    [105,0.997],
    [106,0.997],
    [107,0.997],
    [108,0.997],
    [109,0.997],
    [110,0.997],
    [111,0.997],
    [112,0.997],
    [113,0.981],
    [114,0.981],
    [115,0.981],
    [116,0.981],
    [117,0.981],
    [118,0.981],
    [119,0.981],
    [120,0.981],
    [121,0.981],
    [122,0.981],
    [123,0.981],
    [124,0.981],
    [125,0.981],
    [126,0.981],
    [127,0.981],
    [128,0.981],
    [129,0.981],
    [130,0.981],
    [131,0.981],
    [132,0.981],
    [133,0.981],
    [134,0.981],
    [135,0.981],
    [136,0.981],
    [137,0.981],
    [138,0.981],
    [139,0.981],
    [140,0.981],
    [141,0.981],
    [142,0.981],
    [143,0.981],
    [144,0.981],
    [145,0.981],
    [146,0.981],
    [147,0.981],
    [148,0.981],
    [149,0.981],
    [150,0.981],
    [151,0.981],
    [152,0.981],
    [153,0.981],
    [154,0.981],
    [155,0.965],
    [156,0.965],
    [157,0.965],
    [158,0.965],
    [159,0.965],
    [160,0.965],
    [161,0.965],
    [162,0.965],
    [163,0.965],
    [164,0.965],
    [165,0.965],
    [166,0.965],
    [167,0.965],
    [168,0.965],
    [169,0.965],
    [170,0.965],
    [171,0.965],
    [172,0.965],
    [173,0.965],
    [174,0.965],
    [175,0.965],
    [176,0.965],
    [177,0.965],
    [178,0.914],
    [179,0.914],
    [180,0.914],
    [181,0.914],
    [182,0.914],
    [183,0.914],
    [184,0.914]
]

    tz = ZoneInfo("Asia/Taipei")
    today = datetime.now(tz).date()
    insert_work_date = today - timedelta(days=1)

    try:
        cnx = get_connection_pool()
        cursor = cnx.cursor(dictionary=True)
        for eqp_id in eq_ids:
            insert_start_of_window = datetime.combine(insert_work_date, time(7, 0)).replace(tzinfo=tz)
            insert_end_of_window = insert_start_of_window + timedelta(days=1) - timedelta(seconds=1) # 精確到 06:59:59
            insert_statement = generate_insert_eqp_info_sql(
                eqp_id[0], 
                insert_work_date, 
                insert_start_of_window, 
                insert_end_of_window,
                eqp_id[1] * 70071,
                eqp_id[1] * 76810
                )
            
            cursor.execute(insert_statement)
            cnx.commit()
            print(f'INSERT {eqp_id} 在 {insert_work_date} 成功')
    except Exception as e:
        print(e)

    finally:
        try:
            cursor.close()
            cnx.close()
            print('--------------結束---------------')
        except:
            pass

