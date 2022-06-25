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

###########################################################################

    def getAllNews(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor2 = self.connection.cursor(dictionary=True)

        sql = "SELECT * FROM news WHERE archives = %s AND deleted = %s"
        cursor.execute(sql,[int(0), int(0)])

        news = []
        for data in cursor.fetchall():
            sql = "SELECT * FROM files WHERE idNews = %s AND deleted = %s"
            cursor2.execute(sql, [int(data['id']), int(0)])

            files = []
            for data2 in cursor2.fetchall():
                files.append({
                    "id" : data2['id'],
                    "name" : data2['name']
                })
            
            news.append({
                "id" : data['id'],
                'Desc': data['descc'],
                'Date': data['date'],
                'Files': files
            })
        
        cursor.close()
        cursor2.close()

        return {
            "status": "success",
            "data": news
        }

    def getNewsLifetime(self, idNews):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news WHERE id = %s AND deleted = %s"
        cursor.execute(sql,[int(idNews), int(0)])
        data = cursor.fetchone()

        if data:
            return {
                "status": "success",
                "message": "News found!"
            }
        else:
            return {
                "status": "error",
                "message": "No news found!"
            }
    
    def getNewsById(self, idNews):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news WHERE id = %s AND deleted = %s"
        cursor.execute(sql,[int(idNews), int(0)])
        data = cursor.fetchone()

        sql = "SELECT * FROM files WHERE idNews = %s AND deleted = %s"
        cursor.execute(sql,[int(idNews), int(0)])
        files = []

        for data2 in cursor.fetchall():
            files.append({
                "id" : data2['id'],
                "name" : data2['name']
            })
        
        return {
            "status": "success",
            "data":{
                "id" : data['id'],
                'Desc': data['descc'],
                'Date': data['date'],
                'Files': files
            }
        }
    
    def addNews(self, fileList, desc):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO news (`descc`, `date`, `archived`, `deleted`) VALUES (%s, CURRENT_TIMESTAMP, 0, 0)"
        cursor.execute(sql,[desc, ])
        self.connection.commit()
        id = cursor.lastrowid

        for i in range(len(fileList)):
            sql = 'INSERT INTO files (`idNews`, `name`, `deleted`) VALUES (%s, %s, 0)'
            cursor.execute(sql, [int(id), str(fileList[i])])
            self.connection.commit()
        
        cursor.close()

        return{
            "status": "success",
            "message": "Your news has been created!"
        }
    
    def editNews(self, idNews, desc):
        cursor = self.connection.cursor(dictionary=True)
        sql = 'UPDATE news SET descc = %s WHERE id = %s'
        cursor.execute(sql,[desc, idNews])

        self.connection.commit()
        cursor.close()

        return{
            "status": "success",
            "message": "Your changes has been saved!"
        }
    
    def deleteNews(self, idNews):
        cursor = self.connection.cursor(dictionary=True)
        sql = 'UPDATE news SET deleted = 1 WHERE id = %s'
        cursor.execute(sql,[idNews,])
        self.connection.commit()

        sql = 'UPDATE files SET deleted = 1 WHERE idNews = %s'
        cursor.execute(sql,[idNews,])
        self.connection.commit()

        cursor.close()

        return{
            "status": "success",
            "message": "Your news has been deleted!"
        }

    def downloadFileById(self, idFile):
        cursor = self.connection.cursor(dictionary=True)
        sql = 'SELECT * FROM files WHERE id = %s AND deleted = 0'
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