from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

dbconfig = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "use_pure": True 
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    pool_reset_session=True,
    **dbconfig
)

def get_connection_pool():
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            return connection
        else:
            return connection_pool.get_connection()
    except Exception as e:
        print(e)
        return None