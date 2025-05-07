from connect import get_connection_pool
from mysql.connector import errorcode
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
DB_NAME = os.getenv("MYSQL_DATABASE")
TABLES = {}

TABLES['img_text_posts'] = (
   "CREATE TABLE img_text_posts ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `msg_text` VARCHAR(255) NOT NULL,"
    "  `image_url` VARCHAR(255) NOT NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


cnx = get_connection_pool()
cursor = cnx.cursor(dictionary=True)

def create_database(cursor):
    try:
        cnx = get_connection_pool()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def check_database():
    try:
        cnx = get_connection_pool()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("USE {}".format(DB_NAME))
        cursor.close()
        cnx.close()  
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
            cursor.close()
            cnx.close()  
        else:
            print(err)
            exit(1)

def create_tables():
    cnx = get_connection_pool()
    cursor = cnx.cursor(dictionary=True)
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
    cnx.close()  

def mysql_main():
    check_database()
    create_tables()

if __name__ == "__main__":
    mysql_main()