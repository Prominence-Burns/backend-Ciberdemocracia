import sqlite3

conn = sqlite3.connect('electoral.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

print('Tablas creadas:')
for tabla in cursor.fetchall():
    print(' -', tabla[0])

conn.close()