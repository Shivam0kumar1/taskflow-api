import sqlite3

def get_connection():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row #access columns by name
    return conn

