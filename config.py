import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kanasu@#2906",
        database="hospital_management"
    )
    return connection