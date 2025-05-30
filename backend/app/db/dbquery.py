from backend.app.db.connect import get_connection_pool

def insert_text_img_data(msg_text: str, image_url: str):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        insert_query = """
            INSERT INTO `img_text_posts` (
                `msg_text`,
                `image_url`

            ) VALUES (%s, %s)
            """
        cursor.execute(insert_query, (msg_text, image_url))
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

def get_text_img_data():
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        select_query = """
            SELECT * FROM `img_text_posts` ORDER BY `creation_time` DESC
            """
        cursor.execute(select_query)
        results = cursor.fetchall()

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


def get_avail_data():
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        select_query = """
            SELECT eq_id, status, SUM(hour_time) AS avail_hours
            FROM eqp_status_test 
            WHERE work_date = '2025-05-17' AND
            status = 'run'
            GROUP BY eq_id, status 
            ORDER BY eq_id, status;
            """
        cursor.execute(select_query)
        results = cursor.fetchall()

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
        prod_name: str = None,
        eqp_type: str = None,
        station_name: str = None,
        module_name: str = None,
        creation_time: str = None,
        page: int = 0,
        ):
    page_size: int = 10
    
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
            WHERE 1=1
        """

        count_sql = """
            SELECT COUNT(st.id)
            FROM
                standard_times AS st
            INNER JOIN prod_info AS pi ON st.prod_id = pi.id
            INNER JOIN eqp_types AS et ON st.eqp_type_id = et.id
            INNER JOIN station_info AS si ON st.station_id = si.id
            WHERE 1=1
        """

        conditions = []
        params = {}

        if prod_code:
            conditions.append("pi.prod_code LIKE %s")
            params["prod_code"] = f"%{prod_code}%"
        if prod_name:
            conditions.append("pi.prod_name LIKE %s")
            params["prod_name"] = f"%{prod_name}%"
        if eqp_type:
            conditions.append("et.eqp_type LIKE %s")
            params["eqp_type"] = f"%{eqp_type}%"
        if station_name:
            conditions.append("si.station_name LIKE %s")
            params["station_name"] = f"%{station_name}%"
        if module_name:
            conditions.append("si.module_name LIKE %s")
            params["module_name"] = f"%{module_name}%"
        if creation_time:
            conditions.append("DATE(st.creation_time) = %s")
            params["creation_time"] = creation_time 

        if conditions:
            base_sql += " AND " + " AND ".join(conditions)
            count_sql += " AND " + " AND ".join(conditions)

        
        cursor.execute(count_sql, tuple(params.values()))
        total_records = cursor.fetchone()['COUNT(st.id)']
        total_pages = (total_records + page_size - 1) // page_size
        
        
        start_num = (page - 1) * page_size
        base_sql += "ORDER BY st.id LIMIT %s OFFSET %s"
        params_list = list(params.values()) + [page_size, start_num]

        cursor.execute(base_sql, tuple(params_list))
        results = cursor.fetchall()

        next_page = page + 1 if len(results) == page_size else None

        return [total_pages, next_page, results]

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def query_all_standard_times(
        prod_code: str = None,
        prod_name: str = None,
        eqp_type: str = None,
        station_name: str = None,
        module_name: str = None,
        creation_time: str = None,
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
            WHERE 1=1
        """

        count_sql = """
            SELECT COUNT(st.id)
            FROM
                standard_times AS st
            INNER JOIN prod_info AS pi ON st.prod_id = pi.id
            INNER JOIN eqp_types AS et ON st.eqp_type_id = et.id
            INNER JOIN station_info AS si ON st.station_id = si.id
            WHERE 1=1
        """

        conditions = []
        params = {}

        if prod_code:
            conditions.append("pi.prod_code LIKE %s")
            params["prod_code"] = f"%{prod_code}%"
        if prod_name:
            conditions.append("pi.prod_name LIKE %s")
            params["prod_name"] = f"%{prod_name}%"
        if eqp_type:
            conditions.append("et.eqp_type LIKE %s")
            params["eqp_type"] = f"%{eqp_type}%"
        if station_name:
            conditions.append("si.station_name LIKE %s")
            params["station_name"] = f"%{station_name}%"
        if module_name:
            conditions.append("si.module_name LIKE %s")
            params["module_name"] = f"%{module_name}%"
        if creation_time:
            
            conditions.append("DATE(st.creation_time) = %s")
            params["creation_time"] = creation_time 

        if conditions:
            base_sql += " AND " + " AND ".join(conditions)
            count_sql += " AND " + " AND ".join(conditions)

        
        
        base_sql += "ORDER BY st.id"
        params_list = list(params.values())

        cursor.execute(base_sql, tuple(params_list))
        results = cursor.fetchall()

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


def check_unread_notifications(user_id: int):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        query = """
        SELECT us.user_id, us.is_read, nt.* 
        FROM user_notifications us LEFT JOIN notifications nt 
        on us.notification_id = nt.id
        WHERE 
        us.user_id = %s 
        AND
        is_read = FALSE
        ORDER BY nt.creation_time, nt.id;
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        return rows

    except Exception as e:
        print(f"check_unread_notifications 錯誤: {e}")
        return False
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def get_all_user_ids():
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        query = """
            SELECT id FROM users
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        return [row['id'] for row in rows]

    except Exception as e:
        print(f"錯誤: {e}")
        return []
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass


def get_one_user_notifications(user_id):
    query = """
        SELECT nt.id, nt.title, nt.message, nt.event_type, nt.creation_time
        FROM notifications nt
        JOIN user_notifications us ON nt.id = us.notification_id
        WHERE us.user_id = %s
        ORDER BY nt.creation_time DESC
    """
    try:
        cxn = get_connection_pool()
        cursor = cxn.cursor(dictionary=True)
        cursor.execute(query, (user_id,))
        notifications = cursor.fetchall()
        return notifications

    except Exception as e:
        print(f"get_one_user_notifications() Unexpected error: {e}")
        return []
    finally:
        cursor.close()
        cxn.close()   