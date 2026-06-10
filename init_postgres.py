import psycopg2
from config import DATABASE_URL

def init_postgresql():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        title TEXT,
        description TEXT,
        status VARCHAR(50),
        user_id INT,
        CONSTRAINT fk_jobs_user FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()

    print("PostgreSQL tables created successfully")