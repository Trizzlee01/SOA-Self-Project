from nameko.rpc import rpc
import dependencies.database as db

class SimpleCloudStorageAccountService:

    name = 'simple_cloud_storage_account_service'

    database = db.DatabaseProvider()

    @rpc
    def register(self, userData):
        return self.database.register(userData)
    
    @rpc
    def login(self, userData):
        return self.database.login(userData)

class SimpleCloudStorageDataService:

    name = 'simple_cloud_storage_data_service'

    database = db.DatabaseProvider()

    @rpc
    def uploadFile(self, fileList):
        return self.database.uploadFile(fileList)
    
    @rpc
    def downloadFile(self, idFile):
        return self.database.downloadFile(idFile)

