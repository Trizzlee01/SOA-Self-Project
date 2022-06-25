from nameko.rpc import rpc
import dependencies.database as db

class DepartmentNewsBoardAccountService:

    name = 'department_news_board_account_service'

    database = db.DatabaseProvider()

    @rpc
    def register(self, userData):
        return self.database.register(userData)
    
    @rpc
    def login(self, userData):
        return self.database.login(userData)

class DepartmentNewsBoardNewsService:

    name = 'department_news_board_news_service'

    database = db.DatabaseProvider()

    @rpc
    def getAllNews(self):
        allNews = self.database.getAllNews()
        return allNews

    @rpc
    def getNewsById(self, idNews):
        News = self.database.getNewsById(idNews)
        return News

    @rpc
    def addNews(self, fileList, desc):
        status = self.database.addNews(fileList, desc)
        return status

    @rpc
    def editNews(self, idNews, desc):
        status = self.database.editNews(idNews, desc)
        return status

    @rpc
    def deleteNews(self, idNews):
        status = self.database.deleteNews(idNews)
        return status

    @rpc
    def downloadFileById(self, idFile):
        file = self.database.downloadFileById(idFile)
        return file

    @rpc
    def getNewsLifetime(self, idNews):
        NewsLifetime = self.database.getNewsLifetime(idNews)
        return NewsLifetime
    


