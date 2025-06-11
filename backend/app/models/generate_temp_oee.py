from backend.app.db.connect import get_connection_pool
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

def query_eqp_wip(eqp_id, work_date):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        query_eqp_wip_sql = """
            SELECT ew.eqp_id, ei.eqp_code, ei.eqp_type_id, ew.prod_id, ew.work_date, ew.wip_qty
            FROM eqp_wip ew
            JOIN eqp_info ei ON ew.eqp_id = ei.id
            WHERE ew.eqp_id = %s
            AND ew.work_date = %s
            """
        cursor.execute(query_eqp_wip_sql, (eqp_id, work_date))
        eqp_wip_data = cursor.fetchall()

        return eqp_wip_data

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def query_avail_rate(eqp_id, work_date):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        query_eqp_avail_rate_sql = """
            SELECT si.id AS station_id, 
            si.station_name, 
            ei.eqp_type_id, 
            et.eqp_type, 
            ei.id AS eqp_id,
            ei.eqp_code, 
            format(SUM(es.hours)/24 * 100, 2) AS `avail_rate`, 
            es.work_date, 
            st.status_name 
            FROM eqp_status es
            JOIN eqp_info ei ON es.eqp_id = ei.id
            JOIN station_info si ON ei.station_id = si.id
            JOIN status_types st ON es.status_id = st.id
            JOIN eqp_types et ON ei.eqp_type_id = et.id 
            WHERE 
            st.id = 1
            AND ei.id = %s
            AND work_date = %s
            GROUP BY ei.eqp_code, es.work_date, st.status_name
            ORDER BY si.id, ei.eqp_type_id, es.work_date, ei.eqp_code;
            """
        cursor.execute(query_eqp_avail_rate_sql, (eqp_id, work_date))
        eqp_avail_rate_data = cursor.fetchone()

        return eqp_avail_rate_data

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def query_stdt(prod_id, eqp_type_id):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        query_stdt_sql = """
            SELECT *
            FROM standard_times
            WHERE prod_id = %s
            AND eqp_type_id = %s
            """
        cursor.execute(query_stdt_sql, (prod_id, eqp_type_id))
        prod_stdt = cursor.fetchone()

        return prod_stdt.get("standard_time_value")

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def get_date_info(date_obj):
    try:
        # date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        year = date_obj.year
        month = date_obj.month
        
        week_number_sunday_start = int(date_obj.strftime('%U')) + 1
        
        return {
            "year": year,
            "month": month,
            "week_number": f"W{week_number_sunday_start if week_number_sunday_start >9 else "0" + str(week_number_sunday_start) }",
        }
    except ValueError:
        return {"error": "日期格式不正確，請使用YYYY-MM-DD 格式。"}

def insert_to_oee(eqp_id, eqp_code, station_name, work_date, oee_rate, avail_rate, perf_rate):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        module_dict = {
            "CPU":"FE",
            "RAM":"FE",
            "ROM":"FE",
            "GPU":"FE",
            "PSU":"ME",
            "CLS":"ME",
            "CWG":"ME",
            "CCA":"ME",
            "SIT":"BE",
            "PKG":"BE",
        }

        date_info = get_date_info(work_date)

        insert_query = """
            INSERT INTO `final_oee`
            (
                `eqp_id`,
                `eqp_code`,
                `station_name`,
                `module_name`,
                `year`,
                `month`,
                `week`,
                `work_date`,
                `oee_rate`,
                `avail_rate`,
                `perf_rate`
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(insert_query, (eqp_id, eqp_code, station_name, module_dict.get(station_name), date_info.get("year"), date_info.get("month"), date_info.get("week_number"), work_date, oee_rate, avail_rate, perf_rate))
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

def insert_to_temp_oee(eqp_code, station_name, work_date, oee_rate, avail_rate, perf_rate):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        module_dict = {
            "CPU":"FE",
            "RAM":"FE",
            "ROM":"FE",
            "GPU":"FE",
            "PSU":"ME",
            "CLS":"ME",
            "CWG":"ME",
            "CCA":"ME",
            "SIT":"BE",
            "PKG":"BE",
        }

        date_info = get_date_info(work_date)

        insert_query = """
            INSERT INTO `temp_oee`
            (
                `eqp_code`,
                `station_name`,
                `module_name`,
                `year`,
                `month`,
                `week`,
                `work_date`,
                `oee_rate`,
                `avail_rate`,
                `perf_rate`
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(insert_query, (eqp_code, station_name, module_dict.get(station_name), date_info.get("year"), date_info.get("month"), date_info.get("week_number"), work_date, oee_rate, avail_rate, perf_rate))
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

def generate_temp_oee():
    eq_ids = [2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184]
    tz = ZoneInfo("Asia/Taipei")
    today = datetime.now(tz).date()
    work_date = today - timedelta(days=1)

    for eqp_id in eq_ids:
            
        avail_rate_data = query_avail_rate(eqp_id, work_date) # dict
        avail_rate = avail_rate_data.get("avail_rate")
        avail_mins = float(avail_rate) * 1440 / 100
        eqp_type_id = avail_rate_data.get("eqp_type_id")
        eqp_code = avail_rate_data.get("eqp_code")
        station_name = avail_rate_data.get("station_name")

        # 開始計算作業效率
        eqp_wip_data = query_eqp_wip(eqp_id, work_date) # list，因為機台會作業多種產品
        wip_operation_mins = 0
        for prod_id in eqp_wip_data:
            wip_operation_mins += query_stdt(prod_id.get("prod_id"), eqp_type_id) * prod_id.get("wip_qty")
        
        perf_rate = round(float(wip_operation_mins) / avail_mins * 100, 2)

        oee_rate = round(float(avail_rate) * perf_rate / 100 ,2)

        
        insert_to_temp_oee(eqp_code, station_name, work_date, oee_rate, avail_rate, perf_rate)
        print(f"{eqp_code} 在 {work_date} 的 OEE 為 {oee_rate}%，AR 為 {avail_rate}%，PR 為{perf_rate}%")

