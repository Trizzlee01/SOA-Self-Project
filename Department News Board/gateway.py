import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from dependencies.redis import SessionProvider
import os
from flask import Flask, send_from_directory
from werkzeug.utils import secure_filename

PATH = 'data/news'

EXTENSION_HEADER = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif'
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PATH

if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists(PATH):
    os.mkdir(PATH)

class DepartmentNewsBoardGatewayService:
    name = 'department_news_board_gateway'
    department_news_board_account_rpc = RpcProxy('department_news_board_account_service')
    department_news_board_news_rpc = RpcProxy('department_news_board_news_service')
    session_provider = SessionProvider()
    ### BELOW IS AN AUTOMATICALLY GENERATED FUNCTION TEMPLATES ###
    
    @http('POST', '/register')
    def register(self, request):
        cookies = request.cookies
        if cookies:
            response = Response('Anda sudah login, logout untuk register')
            return response

        else:
            userData = request.get_data(as_text=True)
            userData = json.loads(userData)

            registerStatus = self.student_paper_board_account_rpc.register(userData)

            response = Response(
                json.dumps(registerStatus),
                mimetype='application/json'
            )

            return response

    @http('GET', '/login')
    def login(self, request):
        cookies = request.cookies
        if cookies:
            response = Response('Anda sudah login, logout untuk login ulang')
            return response

        else:
            userData = request.get_data(as_text=True)
            userData = json.loads(userData)

            loginStatus = self.student_paper_board_account_rpc.login(userData)

            response = Response(
                json.dumps(loginStatus),
                mimetype='application/json'
            )

            if loginStatus['status'] == "success":
                sessionId = self.session_provider.setSession(userData)
                response.set_cookie('SESSID', sessionId)
            
            return response

    @http('GET', '/logout')
    def logout(self, request):
        cookies = request.cookies

        if cookies:
            self.session_provider.logout(cookies['SESSID'])

            status = {
                "status": "success",
                "message": "Log out success! "
            }
            response.delete_cookie('SESSID', sessionId)
            response = Response(
                json.dumps(status),
                mimetype='application/json'
            )

            return response

        else:
            response = Response('Anda belum login')
            return response

    @http('GET', '/getAllNews')
    def getAllNews(self,request):
        allNews = self.department_news_board_news_rpc.getAllNews()

        response = Response(
            json.dumps(allNews),
            mimetype='application/json'
        )

        return response
    
    @http('GET', '/news/<int:idNews>')
    def getNewsById(self, request, idNews):
        newsLifeTime = self.department_news_board_news_rpc.getNewsLifetime(idNews)

        if newsLifeTime['status'] == "success":
            News = self.department_news_board_news_rpc.getNewsById(idNews)
            result = News
        else:
            result = newsLifeTime
            
        response = Response(
            json.dumps(result),
            mimetype='application/json'
        )
        return response


    @http ('POST', '/news')
    def addNews(self, request):
        cookies = request.cookies

        if cookies:
            files = request.files.getlist('file')
            fileList = []
            for data in files:

                fileName = secure_filename(data.filename)
                data.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
                
                fileList.append(fileName)

            status = self.department_news_board_news_rpc.addNews(fileList)

            response = Response(
                json.dumps(status),
                mimetype='application/json'
            )

            return response
        else:
            response = Response('Anda belum login')
            return response

    @http ('PUT', '/news/<int:idNews>')
    def editNews(self, request, idNews):
        cookies = request.cookies

        if cookies:
            newsLifeTime = self.department_news_board_news_rpc.getNewsLifetime(idNews)

            if newsLifeTime['status'] == "success":
                data = request.get_data(as_text=True)
                data = json.loads(data)

                status = self.department_news_board_news_rpc.editNews(idNews, data)
                result = status
            else:
                result = newsLifeTime

            response = Response(
                json.dumps(result),
                mimetype='application/json'
            )
            return response
        else:
            response = Response('Anda belum login')
            return response

    @http ('DELETE', '/news/<int:idNews>')
    def deleteNews(self, request, idNews):
        cookies = request.cookies

        if cookies:
            newsLifeTime = self.department_news_board_news_rpc.getNewsLifetime(idNews)

            if newsLifeTime['status'] == "success":

                status = self.department_news_board_news_rpc.deleteNews(idNews)
                result = status
            else:
                result = newsLifeTime

            response = Response(
                json.dumps(result),
                mimetype='application/json'
            )
            return response
        else:
            response = Response('Anda belum login')
            return response

    @http('GET', 'news/file/<int:idFile>')
    def downloadFileById(self, request, idFile):
        download = self.department_news_board_news_rpc.downloadFileById(idFile)

        if download['status']=="success":
            name = download['data']['name']
            response = Response(open(PATH + '/' + name, 'rb').read())
            fileType = name.split('.')[-1]
            
            response.headers['Content-Type'] = EXTENSION_HEADER[fileType]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(name)
        else:
            result = download
            response = Response(
                json.dumps(result),
                mimetype='application/json'
            )

        return response
        




