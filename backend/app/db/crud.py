from backend.app.db.connect import get_connection_pool
import mysql.connector
from dotenv import load_dotenv
import os
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Request
from datetime import datetime

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
        print(f"錯誤: {e}")
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
        if not auth_header.startswith("Bearer "):
            return None
        
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
        print(e)
        return False

async def get_current_active_user(request: Request):
    return await get_current_user(request)

