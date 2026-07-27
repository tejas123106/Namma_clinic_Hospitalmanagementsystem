from config import get_db_connection

try:
    conn = get_db_connection()

    print("Connected Successfully!")

    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Current Database:", cursor.fetchone())

    conn.close()

except Exception as e:
    print(type(e))
    print(e)