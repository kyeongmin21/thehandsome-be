import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",      # 로컬 MySQL
            user="root",           # MySQL 계정
            password="1204",   # MySQL 비밀번호
            database="project"   # 사용할 DB 이름
        )
        if conn.is_connected():
            print("MySQL 연결 성공 ✅")
            return conn
    except Error as e:
        print("MySQL 연결 실패:", e)
        return None

# 사용 예시
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        print(cursor.fetchall())
        cursor.close()
        conn.close()