import sqlite3
print('SQLite version:', sqlite3.version)
try:
    conn = sqlite3.connect('data.db')
    print('Connected to database successfully')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('Tables in database:', tables)
    conn.close()
except Exception as e:
    print('Database connection error:', e)