from backend.app.db.connect import get_connection_pool
from fastapi import Request, HTTPException, status
import mysql.connector
from dotenv import load_dotenv
import os
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone, date
from fastapi import Request
from sqlalchemy import text
from pydantic import BaseModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

cnx = get_connection_pool()
cursor = cnx.cursor(dictionary=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserForm:
    def __init__(self, account, password, name, position):
        self.account = account
        self.password = password
        self.name = name
        self.position = position
        
    def insert_user(self):
        try:
            cnx = get_connection_pool()
            cursor = cnx.cursor()

            insert_query = (
                "INSERT INTO `users` (`account`, `password`, `name`, `position`) "
                "VALUES (%s, %s, %s, %s)"
            )

            cursor.execute(insert_query, (self.account, self.password, self.name, self.position))
            cnx.commit()

            print(f"User {self.account} inserted successfully.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            cnx.rollback()

        finally:
            try:
                cursor.close()
                cnx.close()
            except:
                pass

def check_user(new_account):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        query = "SELECT id, account, password, name, position FROM users WHERE account = %s"
        cursor.execute(query, (new_account,))
        existing_user = cursor.fetchone()  

        if existing_user:  
            print("account 存在...")
            return existing_user
        else:
            print("回傳 None...")
            return None

    except Exception as e:
        print(f"check_user 錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def query_user_data(user_id):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        query = "SELECT id, account, password, name, position FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        existing_user = cursor.fetchone()  

        if existing_user:  
            print("id 存在...")
            return existing_user
        else:
            print("回傳 None...")
            return None

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_current_user(request: Request):

    try:
        auth_header = request.headers.get("Authorization")
        print(f"get_current_user: auth_header = {auth_header}")
            
        if auth_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header invalid (expected Bearer token)",
                headers={"WWW-Authenticate": "Bearer"},
            )

        
        token = auth_header.split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        username: str = payload.get("username")
        account: str = payload.get("account")
        user_id: int = payload.get("user_id")
        if username is None or account is None or user_id is None:
            return None
        user = check_user(account)  
        return user
    except Exception as e:
        print(f"get_current_user 發生錯誤：{e}")
        return False

async def get_current_active_user(request: Request):
    return await get_current_user(request)

class StandardTimeUpdate(BaseModel):
    prod_code: str
    eqp_type: str
    station_name: str
    stdt: float

def update_standard_time_value(item):
    try:
        cnx = get_connection_pool()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
                    """
                    SELECT st.id
                    FROM standard_times st
                    JOIN prod_info p ON p.prod_code = %s AND p.id = st.prod_id
                    JOIN eqp_types e ON e.eqp_type = %s AND e.id = st.eqp_type_id
                    JOIN station_info s ON s.station_name = %s AND s.id = st.station_id
                    """,
                    (item.get("prod_code"), item.get("eqp_type"), item.get("station_name"))
                )
        result = cursor.fetchone()
        print(f"查詢欲更新的資料的結果: {result}")
        if not result:
            print(f"找不到符合條件的資料: {item.get("prod_code")}, {item.get("eqp_type")}, {item.get("station_name")}")
            return False

        standard_time_id = result["id"]
        cursor.execute(
            "UPDATE standard_times SET standard_time_value = %s WHERE id = %s",
            (item.get("stdt"), standard_time_id)
        )
        cnx.commit()
        print(f"成功更新標準時間: {item.get("prod_code")}, {item.get("eqp_type")}, {item.get("station_name")} {item.get("stdt")}")


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()
    
    except Exception as e:
        print(f"發生錯誤{e}")

    finally:
        try:
            cursor.close()
            cnx.close()
            return True
        except Exception as e:
            print(f"Error closing connection: {e}")
            pass

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token 已過期")
        return None
    except jwt.InvalidTokenError:
        print("無效的 Token")
        return None
    except Exception as e:
        print(f"解碼 Token 時發生錯誤: {e}")
        return None
       
def create_notification_and_assign_users(notification, user_ids):
    query_notif = """
        INSERT INTO notifications (title, message, event_type)
        VALUES (%s, %s, %s)
    """
    query_assign = """
        INSERT INTO user_notifications (user_id, notification_id)
        VALUES (%s, %s)
    """
    try:
        cxn = get_connection_pool()
        cursor = cxn.cursor()
        cursor.execute(query_notif, (notification.title, notification.message, notification.event_type))
        notif_id = cursor.lastrowid

        for user_id in user_ids:
            cursor.execute(query_assign, (user_id, notif_id))
        cxn.commit()

        return notif_id
    except mysql.connector.Error as err:
        print(f"create_notification_and_assign_users() Error: {err}")
        cxn.rollback()
    
    except Exception as e:
        print(f"create_notification_and_assign_users() Unexpected error: {e}")
        cxn.rollback()
    finally:
        try:
            cursor.close()
            cxn.close()
        except Exception as e:
            print(f"create_notification_and_assign_users Error closing connection: {e}")
            pass

def get_unread_notification_status(user_id):
    query = """
        SELECT COUNT(*) FROM user_notifications
        WHERE user_id = %s AND is_read = FALSE
    """
    try:
        cxn = get_connection_pool()
        cursor = cxn.cursor()
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()[0]
    except mysql.connector.Error as err:
        print(f"get_unread_notification_status() Error: {err}")
        count = 0
    except Exception as e:
        print(f"get_unread_notification_status() Unexpected error: {e}")
        count = 0
    finally:
        cursor.close()
        cxn.close()
        return count > 0

def mark_all_notifications_read(user_id):
    query = """
        UPDATE user_notifications SET is_read = TRUE
        WHERE user_id = %s AND is_read = FALSE
    """
    try:
        cxn = get_connection_pool()
        cursor = cxn.cursor()
        cursor.execute(query, (user_id,))
        cxn.commit()
    except mysql.connector.Error as err:
        print(f"mark_all_notifications_read() Error: {err}")
        cxn.rollback()
    except Exception as e:
        print(f"mark_all_notifications_read() Unexpected error: {e}")
        cxn.rollback()
    finally:
        cursor.close()
        cxn.close()

def insert_gantt_chart_data(station_name: str, work_date: str, image_url: str):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        query_sql = """
            SELECT id, station_name FROM station_info
            WHERE station_name = %s
            """
        
        cursor.execute(query_sql, (station_name,))
        station_id = cursor.fetchone()
        print(station_id)
        
        insert_query = """
            INSERT INTO `gantt_charts`
            (
                `station_id`,
                `work_date`,
                `image_url`
                )
                VALUES (%s, %s, %s)
            """
        cursor.execute(insert_query, (station_id.get("id"), work_date, image_url))
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

class EqpStatusUpdate(BaseModel):
    id: int
    comment: str

def update_eqp_status_comment(item):
    try:
        cnx = get_connection_pool()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute(
            "UPDATE eqp_status SET comment = %s WHERE id = %s",
            (item.comment, item.id)
        )
        cnx.commit()
        print(f"成功更新 eqp_status {item.id} 的 comment 為：{item.comment} ")


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()
    
    except Exception as e:
        print(f"發生錯誤{e}")

    finally:
        try:
            cursor.close()
            cnx.close()
            return True
        except Exception as e:
            print(f"Error closing connection: {e}")
            pass

def insert_final_oee_data(data: list):
        
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        for row in data:
        
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
            cursor.execute(insert_query, (
                row.get("eqp_id"),
                row.get("eqp_code"),
                row.get("station_name"),
                row.get("module_name"),
                row.get("year"),
                row.get("month"),
                row.get("week"),
                row.get("work_date"),
                row.get("oee_rate"),
                row.get("avail_rate"),
                row.get("perf_rate")
            ))
            cnx.commit()
            print(f"{row.get("eqp_code")} 在 {row.get("work_date")} 的資料 INSERT 成功。")

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass

def delete_temp_oee_data(data: list):
        
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        for row in data:
        
            delete_query = """
                DELETE FROM temp_oee 
                WHERE id = %s;
                """
            cursor.execute(delete_query, (
                row.get("id"),
            ))
            cnx.commit()
            print(f"{row.get("eqp_code")} 在 {row.get("work_date")} 的 temp_oee 資料 DELETE 成功。")

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass


def update_temp_oee_by_eqp_id(eqp_id, work_date, tobe_oee_rate, tobe_perf_rate):
    try:
        cnx = get_connection_pool()
        cursor = cnx.cursor(dictionary=True)

        query_sql = """
            SELECT id, eqp_code, oee_rate, perf_rate FROM temp_oee
            WHERE eqp_id = %s AND work_date = %s      
            """
        print("開始執行 query_sql")
        cursor.execute(
            query_sql,
            (eqp_id, work_date)
        )

        asis_temp_oee_data = cursor.fetchone()
        print("結束執行 query_sql")
        print(f"asis_temp_oee_data: {asis_temp_oee_data}")
        asis_oee_rate = float(asis_temp_oee_data.get("oee_rate"))
        asis_perf_rate = float(asis_temp_oee_data.get("perf_rate"))
        eqp_code = asis_temp_oee_data.get("eqp_code")
        temp_oee_id = asis_temp_oee_data.get("id")

        print("開始執行 UPDATE")
        cursor.execute(
            "UPDATE temp_oee SET oee_rate = %s, perf_rate = %s WHERE id = %s",
            (tobe_oee_rate, tobe_perf_rate, temp_oee_id)
        )

        cnx.commit()
        print(f"更新 temp_oee(id:{temp_oee_id})")
        print(f"ASIS OEE：{asis_oee_rate}，ASIS 作業效率：{asis_perf_rate}。 ")
        print(f"TOBE OEE：{tobe_oee_rate}，TOBE 作業效率：{tobe_perf_rate}。 ")
        print("-"*20)

        updated_dict = {
            "eqp_id": eqp_id,
            "work_date": work_date,
            "eqp_code": eqp_code,
            "asis_oee_rate": asis_oee_rate,
            "asis_perf_rate": asis_perf_rate,
            "tobe_oee_rate": tobe_oee_rate,
            "tobe_perf_rate": tobe_perf_rate,
        }

        return updated_dict

    except Exception as e:
        print(f"update_temp_oee_by_eqp_id 發生錯誤{e}")

    finally:
        try:
            cursor.close()
            cnx.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
            pass 

