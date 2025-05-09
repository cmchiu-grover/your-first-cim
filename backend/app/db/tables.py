from mysql.connector import errorcode
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_ROOT_USER = os.getenv("MYSQL_ROOT_USER")
MYSQL_ROOT_USER_PASSWORD = os.getenv("MYSQL_ROOT_USER_PASSWORD")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE") 
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

TABLES = {}

TABLES['img_text_posts'] = (
   "CREATE TABLE img_text_posts ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `msg_text` VARCHAR(255) NOT NULL,"
    "  `image_url` VARCHAR(255) NOT NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

def check_database():
    try:
        temp_cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT,
            use_pure=True
        )
        temp_cursor = temp_cnx.cursor()
        temp_cursor.execute("USE {}".format(MYSQL_DATABASE))
        print("資料庫 {} 已存在".format(MYSQL_DATABASE))
        temp_cursor.close()
        temp_cnx.close()
        return True

    except mysql.connector.Error as err:
        print("資料庫 {} 不存在".format(MYSQL_DATABASE))
        print(err)
        return None


def create_database():
    try:
        temp_cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_ROOT_USER,
            password=MYSQL_ROOT_USER_PASSWORD,
            port=MYSQL_PORT,
            use_pure=True
        )
        print("連接到 MySQL 成功！")
        temp_cursor = temp_cnx.cursor()

        create_db_query = f"CREATE DATABASE {MYSQL_DATABASE} DEFAULT CHARACTER SET 'utf8mb4'"

        create_user_auth = f"GRANT ALL PRIVILEGES ON `{MYSQL_DATABASE}` . * TO '{MYSQL_USER}'@'{MYSQL_HOST}';"

        print("創建資料庫 {}...".format(MYSQL_DATABASE))
        temp_cursor.execute(create_db_query)

        print("建立使用者 {} 權限...".format(MYSQL_USER))
        temp_cursor.execute(create_user_auth)
        print(f"資料庫 '{MYSQL_DATABASE}' 創建成功！")
    except mysql.connector.Error as err:
        print("資料庫創建失敗: {}".format(err))
        exit(1)
    finally:
        temp_cursor.close()
        temp_cnx.close()

def create_tables():
    temp_cnx = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT,
        use_pure=True
    )
    temp_cursor = temp_cnx.cursor(dictionary=True)
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("創建 table {}: ".format(table_name), end='')
            temp_cursor.execute(table_description)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table 已經存在")
            else:
                print(err.msg)
        else:
            print("OK")
    temp_cnx.close()
    temp_cursor.close()

def mysql_main():
    if check_database():
        print("資料庫已存在，檢查表格...")
        create_tables()
    else:
        print("資料庫不存在，創建資料庫...")
        create_database()
        create_tables()

if __name__ == "__main__":
    mysql_main()