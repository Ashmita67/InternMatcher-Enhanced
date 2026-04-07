import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False, fetchall=False, commit=False):
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query, params)
        if commit:
            connection.commit()
            result = cursor.lastrowid
        elif fetchall:
            result = cursor.fetchall()
        elif fetch:
            result = cursor.fetchone()
    except Error as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        connection.close()
    
    return result
