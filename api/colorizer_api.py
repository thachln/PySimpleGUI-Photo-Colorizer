from flask_appbuilder.api import BaseApi, expose

class ColorizerApi(BaseApi):
    @expose('/')
    def help(self):
        return self.response(200, message="Welcome to Colorizer API.")