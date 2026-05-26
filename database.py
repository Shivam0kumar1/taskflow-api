import sqlite3
from config import DATABASE_URL

def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row #access columns by name
    return conn

