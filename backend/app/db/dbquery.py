from app.db.connect import get_connection_pool

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