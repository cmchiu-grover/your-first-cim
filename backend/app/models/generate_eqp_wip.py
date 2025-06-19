from backend.app.db.connect import get_connection_pool
import random
import json
import math
import datetime
from datetime import timedelta
import random
import json
import math
import datetime
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
import os

def query_avail_mins(eqp_code, work_date):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        base_sql = """
            SELECT si.id, 
            si.station_name, 
            ei.eqp_type_id, 
            ei.eqp_code, 
            format(SUM(es.hours)*60, 2) AS `avail_min`,
            es.work_date, st.status_name 
            FROM eqp_status es
            JOIN eqp_info ei ON es.eqp_id = ei.id
            JOIN station_info si ON ei.station_id = si.id
            JOIN status_types st ON es.status_id = st.id
            WHERE st.id = 1 AND ei.eqp_code = %s AND work_date = %s
            GROUP BY ei.eqp_code, es.work_date, st.status_name
            ORDER BY si.id, ei.eqp_type_id, es.work_date, ei.eqp_code;
        """

        cursor.execute(base_sql, (eqp_code, work_date))
        results = cursor.fetchone()

        return results

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def query_standard_times(
        prod_code: str = None,
        eqp_type: str = None,
        ):

    
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        base_sql = """
            SELECT
                st.id AS standard_time_id,
                pi.prod_code,
                pi.prod_name,
                et.eqp_type,
                si.module_name,
                si.station_name,
                st.standard_time_value,
                st.description AS standard_time_description,
                st.creation_time,
                st.updated_time
            FROM
                standard_times AS st
            INNER JOIN
                prod_info AS pi ON st.prod_id = pi.id
            INNER JOIN
                eqp_types AS et ON st.eqp_type_id = et.id
            INNER JOIN
                station_info AS si ON st.station_id = si.id
            WHERE pi.prod_code = %s AND et.id = %s
        """


        cursor.execute(base_sql, (prod_code, eqp_type))
        results = cursor.fetchone()


        return results

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def insert_eqp_wip(eqp_code, work_date, product_code, insert_qty):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        query_eqp_id_sql = """
            SELECT id FROM eqp_info
            WHERE eqp_code = %s
            """
        cursor.execute(query_eqp_id_sql, (eqp_code,))
        eqp_id = cursor.fetchone().get("id")

        query_prod_id_sql = """
            SELECT id FROM prod_info
            WHERE prod_code = %s
            """
        cursor.execute(query_prod_id_sql, (product_code,))
        prod_id = cursor.fetchone().get("id")

        insert_query = """
            INSERT INTO `eqp_wip`
            (
                `eqp_id`,
                `prod_id`,
                `work_date`,
                `wip_qty`
                )
                VALUES (%s, %s, %s, %s)
            """
        cursor.execute(insert_query, (eqp_id, prod_id, work_date, insert_qty))
        cnx.commit()

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def generate_eqp_wip():
    print("開始產生 WIP 資料")
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, 'standard_qty.json')
    # 載入標準工時 JSON 檔
    with open(json_path, 'r', encoding='utf-8') as jsonfile:
        eqp_data_list = json.load(jsonfile)

    tz = ZoneInfo("Asia/Taipei")
    today = datetime.now(tz).date()
    work_date = today - timedelta(days=1)
    
    for eqp in eqp_data_list:
        eqp_code = eqp.get("eqp_code")
        eqp_type_id = eqp.get("eqp_type_id")
        avail_mins = float(query_avail_mins(eqp_code, work_date).get("avail_min").replace(',',''))
        target_avail_mins = random.uniform(850, 950) / 1000 * avail_mins

        std_times = eqp.get("std_times", {})
        total_qty = sum(std_times.values())  # 所有產品的數量總和
        
        for product_code, qty in std_times.items():
                prod_time = float(query_standard_times(product_code, eqp_type_id)["standard_time_value"])
                if prod_time == 0:
                    print(f"{product_code} 的標準時間為 0，跳過")
                    continue

                # 依比例計算分配後的數量（乘上目標可用時間後，除以標準工時）
                ratio = qty / total_qty
                insert_qty = math.ceil((target_avail_mins * ratio) / prod_time)

                print(f'{eqp_code} 在 {work_date} 作業 {product_code}：{insert_qty} 數量')
                insert_eqp_wip(eqp_code, work_date, product_code, insert_qty)

if __name__ == "__main__":
    generate_eqp_wip()