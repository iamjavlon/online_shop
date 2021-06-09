import sqlite3

with sqlite3.connect("db.sqlite3", check_same_thread=False) as conn:
    conn.commit()

cursor = conn.cursor()
