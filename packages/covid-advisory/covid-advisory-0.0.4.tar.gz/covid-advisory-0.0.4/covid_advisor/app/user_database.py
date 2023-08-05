import mysql.connector as mysql
from .config import database_cfg

user_db = mysql.connect(
    host = database_cfg['host'],
    user = database_cfg['user'],
    passwd = database_cfg['passwd'],
    database = database_cfg['database']
)

db_cursor = user_db.cursor()
class Users_DB():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        sql = "INSERT into users (username, password) VALUES (%s, %s)"
        val = (self.username, self.password)
        db_cursor.execute(sql, val)
        user_db.commit()
    
    def findUsername(self):
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (self.username, self.password)
        db_cursor.execute(sql, val)
        return db_cursor.fetchall()[0]
    
    def findID(self, user_id):
        sql = "SELECT * FROM users WHERE id = %s"
        val = (user_id,)
        db_cursor.execute(sql, val)
        return db_cursor.fetchall()[0]
    
    
    


