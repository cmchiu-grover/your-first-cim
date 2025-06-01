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

TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `account`  VARCHAR(255) NOT NULL,"
    "  `password` VARCHAR(255) NOT NULL,"
    "  `name` VARCHAR(255) NOT NULL,"
    "  `position` VARCHAR(255) NOT NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`), "
    "  UNIQUE KEY `unique_account` (`account`),"
    "  INDEX `index_position` (`position`),"
    "  INDEX `index_account_position` (`account`, `position`)"
    ") ENGINE=InnoDB")

TABLES['eqp_types'] = (
    "CREATE TABLE `eqp_types` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `eqp_type` VARCHAR(10) UNIQUE NOT NULL,"
    "  `description` VARCHAR(255),"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['station_info'] = (
    "CREATE TABLE `station_info` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `module_name` VARCHAR(50) NOT NULL,"
    "  `station_name` VARCHAR(50) UNIQUE NOT NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  INDEX `index_module_name` (`module_name`),"
    "  INDEX `index_module_station_name` (`module_name`, `station_name`)"
    ") ENGINE=InnoDB")

TABLES['status_types'] = (
    "CREATE TABLE `status_types` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `status_name` VARCHAR(50) UNIQUE NOT NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['product_categories'] = (
    "CREATE TABLE `product_categories` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `category_name` VARCHAR(50) UNIQUE NOT NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['prod_info'] = (
    "CREATE TABLE `prod_info` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `prod_code` VARCHAR(16) UNIQUE NOT NULL,"
    "  `prod_name` VARCHAR(100) NOT NULL,"
    "  `category_id` INT(11) NOT NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  INDEX `index_prod_name` (`prod_name`),"
    "  UNIQUE INDEX `idx_prod_category_name_code` (`category_id`, `prod_name`, `prod_code`),"
    "  FOREIGN KEY (`category_id`) REFERENCES `product_categories`(`id`)"
    ") ENGINE=InnoDB")

TABLES['standard_times'] = (
    "CREATE TABLE `standard_times` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `prod_id` INT(11) NOT NULL,"
    "  `eqp_type_id` INT(11) NOT NULL,"
    "  `station_id` INT(11) NOT NULL,"
    "  `standard_time_value` DECIMAL(10,4) NOT NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  INDEX `index_eqp_type_id` (`eqp_type_id`),"
    "  INDEX `index_station_id` (`station_id`),"
    "  UNIQUE INDEX `idx_unique_standard_time` (`prod_id`, `eqp_type_id`, `station_id`),"
    "  FOREIGN KEY (`prod_id`) REFERENCES `prod_info`(`id`),"
    "  FOREIGN KEY (`eqp_type_id`) REFERENCES `eqp_types`(`id`),"
    "  FOREIGN KEY (`station_id`) REFERENCES `station_info`(`id`)"
    ") ENGINE=InnoDB")

TABLES['eqp_info'] = (
    "CREATE TABLE `eqp_info` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `eqp_code` VARCHAR(16) UNIQUE NOT NULL,"
    "  `eqp_type_id` INT(11) NOT NULL,"
    "  `station_id` INT(11) NOT NULL,"
    "  `location` VARCHAR(100) NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  INDEX `index_station_id` (`station_id`),"
    "  UNIQUE INDEX `idx_eqp_code_station_unique` (`eqp_code`, `station_id`),"
    "  FOREIGN KEY (`eqp_type_id`) REFERENCES `eqp_types`(`id`),"
    "  FOREIGN KEY (`station_id`) REFERENCES `station_info`(`id`)"
    ") ENGINE=InnoDB")

TABLES['eqp_status'] = (
    "CREATE TABLE `eqp_status` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `eqp_id` INT(11) NOT NULL,"
    "  `work_date` DATE NOT NULL,"
    "  `start_time` DATETIME NOT NULL,"
    "  `end_time` DATETIME NULL,"
    "  `hours` DECIMAL(10,6) NULL,"
    "  `status_id` INT(11) NOT NULL,"
    "  `comment` VARCHAR(255) NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  INDEX `index_work_date` (`work_date`),"
    "  INDEX `index_eqp_id` (`eqp_id`),"
    "  INDEX `index_status_id` (`status_id`),"
    "  INDEX `index_start_time` (`start_time`),"
    "  INDEX `idx_eqp_id_start_time` (`eqp_id`, `start_time`),"
    "  FOREIGN KEY (`eqp_id`) REFERENCES `eqp_info`(`id`),"
    "  FOREIGN KEY (`status_id`) REFERENCES `status_types`(`id`)"
    ") ENGINE=InnoDB")

TABLES['product_routings'] = (
    "CREATE TABLE `product_routings` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `prod_id` INT(11) NOT NULL,"
    "  `station_id` INT(11) NOT NULL,"
    "  `sequence_number` VARCHAR(3) NOT NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  UNIQUE INDEX `idx_prod_station` (`prod_id`, `station_id`),"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`prod_id`) REFERENCES `prod_info`(`id`),"
    "  FOREIGN KEY (`station_id`) REFERENCES `station_info`(`id`)"
    ") ENGINE=InnoDB")

TABLES['work_orders'] = (
    "CREATE TABLE `work_orders` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  `prod_id` INT(11) NOT NULL,"
    "  `qty` INT(11) NOT NULL,"
    "  `order_status` VARCHAR(50) NOT NULL,"
    "  `description` VARCHAR(255) NULL,"
    "  `due_date` DATETIME NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  INDEX `idx_prod_id` (`prod_id`),"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`prod_id`) REFERENCES `prod_info`(`id`)"
    ") ENGINE=InnoDB")

TABLES['notifications'] = (
    "CREATE TABLE `notifications` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  event_type VARCHAR(50),"
    "  title VARCHAR(255),"
    "  message TEXT,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  INDEX `idx_event_type` (`event_type`),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['user_notifications'] = (
    "CREATE TABLE `user_notifications` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  user_id INT,"
    "  notification_id INT,"
    "  is_read BOOLEAN DEFAULT FALSE,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,"
    "  INDEX `idx_user_id` (`user_id`),"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),"
    "  FOREIGN KEY (notification_id) REFERENCES notifications(id)"
    ") ENGINE=InnoDB")

TABLES['gantt_charts'] = (
    "CREATE TABLE `gantt_charts` ("
    "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
    "  station_id INT NOT NULL,"
    "  work_date DATE NOT NULL,"
    "  image_url VARCHAR(255) NOT NULL,"
    "  `creation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  UNIQUE (station_id, work_date),"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`station_id`) REFERENCES `station_info`(`id`)"
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