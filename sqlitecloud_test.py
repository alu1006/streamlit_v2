import sqlitecloud
import db
import dotenv
import os
dotenv.load_dotenv()

conn = sqlitecloud.connect(f"sqlitecloud://cxecbykinz.sqlite.cloud:8860/users?apikey={os.getenv('SQL_KEY')}")

# You can autoselect the database during the connect call
# by adding the database name as path of the SQLite Cloud
# connection string, eg:
# conn = sqlitecloud.connect("sqlitecloud://myhost.sqlite.cloud:8860/mydatabase?apikey=myapikey")
# db_name = "chinook.sqlite"
# conn.execute(f"USE DATABASE {db_name}")

c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)')
# conn.commit()
conn.close()
