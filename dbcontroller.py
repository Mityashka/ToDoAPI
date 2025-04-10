import psycopg2
from configs import host, user, password, db_name

def connect():
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date TIMESTAMP,
            status VARCHAR(50)
        )
        """)

        return connection, cursor
    except Exception as ex:
        print(f"[ERROR] Connection failed: {ex}")
