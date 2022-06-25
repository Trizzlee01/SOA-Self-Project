from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling
import json
class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def register(self, userData):
        username = userData['username']
        password = userData['password']

        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE username = %s"
        cursor.execute(sql,[username,])

        data = cursor.fetchone()
        if data:
            return {
                "status": "error",
                "message": "Username is taken."
            }
        else:
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            cursor.execute(sql,[username, password])
            self.connection.commit()
            return {
                "status": "success",
                "message": "New Account Created!",
                data : {
                    "username" : username,
                    "password" : password
                }
            }
    
    def login(self, userData):
        username = userData['username']
        password = userData['password']

        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(sql,[username, password])
        
        data = cursor.fetchone()
        if data:
            return {
                "status": "success",
                "message": "Login Success!",
                "data":{
                    "username": username
                }
            }
        else:
            return {
                "status": "error",
                "message": "Your credentials do not match our records! "
            }

    def uploadFile(self, name):
        cursor = self.connection.cursor(dictionary=True)
        sql = 'INSERT INTO storage (`name`) VALUES (%s,)'
        cursor.execute(sql,[name,])
        self.connection.commit()
        
        cursor.close()

        return{
            "status": "success",
            "message": "Your file has been uploaded!"
        }

    def downloadFile(self, idFile):
        cursor = self.connection.cursor(dictionary=True)
        sql = 'SELECT * FROM storage WHERE id = %s'
        cursor.execute(sql,[idFile,])
        data = cursor.fetchone()

        if data:
            return {
                "status": "success",
                "data": {
                    'id': data['id'],
                    'name': data['name']
                }
            }
        else:
            return{
                "status": "error",
                "message": "No file found!"
            }

class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='SOA_Mandiri',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())