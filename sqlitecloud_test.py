import sqlitecloud
import db

conn = sqlitecloud.connect("sqlitecloud://cxecbykinz.sqlite.cloud:8860/chinook.sqlite?apikey=1Yf0LpKlXL1VG5K7ky4aeHNDfFeOCqs0WIMP79XSnSo")

# You can autoselect the database during the connect call
# by adding the database name as path of the SQLite Cloud
# connection string, eg:
# conn = sqlitecloud.connect("sqlitecloud://myhost.sqlite.cloud:8860/mydatabase?apikey=myapikey")
db_name = "users"
conn.execute(f"USE DATABASE {db_name}")

cursor = conn.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)')
result = cursor.fetchone()

print(result)

conn.close()