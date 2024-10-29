import sqlite3
import sqlitecloud
import dotenv
import os
dotenv.load_dotenv()
def conn_db(db_name):
    conn = sqlitecloud.connect(f"sqlitecloud://cxecbykinz.sqlite.cloud:8860/{db_name}?apikey={os.getenv('SQL_KEY')}")
    return conn

# 建立使用者資料表
def create_usertable():
    conn = conn_db('users')
    
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

# 新增使用者
def add_user(username, password):
    conn = conn_db('users')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
# add_user('admin', 'admin') 
# 驗證使用者
def login_user(username, password):
    conn = conn_db('users')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchone()
    conn.close()
    return data
    
