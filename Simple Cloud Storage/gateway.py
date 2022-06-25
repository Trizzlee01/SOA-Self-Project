import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from dependencies.redis import SessionProvider
import os
from flask import Flask, send_from_directory
from werkzeug.utils import secure_filename

PATH = 'data/file'

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

class SimpleCloudStorageGatewayService:
    name = 'simple_cloud_storage_gateway'
    simple_cloud_storage_data_rpc = RpcProxy('simple_cloud_storage_data_service')
    simple_cloud_storage_account_rpc = RpcProxy('simple_cloud_storage_account_service')
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

            registerStatus = self.simple_cloud_storage_account_rpc.register(userData)

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

            loginStatus = self.simple_cloud_storage_account_rpc.login(userData)

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
            
            response = Response(
                json.dumps(status),
                mimetype='application/json'
            )
            response.delete_cookie('SESSID')
            return response

        else:
            response = Response('Anda belum login')
            return response
    
    @http('POST', '/storage')
    def uploadFile(self, request):
        files = request.files.getlist('file')
        fileList = []
        for data in files:

            fileName = secure_filename(data.filename)
            data.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
            
            fileList.append(fileName)

        status = self.simple_cloud_storage_data_rpc.uploadFile(fileList)

        response = Response(
            json.dumps(status),
            mimetype='application/json'
        )

        return response

        
    @http('GET', '/storage/<int:idFile>')
    def downloadFile(self, request, idFile):
        download = self.simple_cloud_storage_data_rpc.downloadFile(idFile)

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

