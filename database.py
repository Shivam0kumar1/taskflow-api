import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_URL
from typing import Generator

def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)

def get_db() -> Generator[psycopg2.extensions.connection, None, None]:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()