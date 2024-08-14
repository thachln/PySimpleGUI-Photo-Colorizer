from flask_appbuilder.api import BaseApi, expose

class ColorizerApi(BaseApi):
    route_base = "api/colorizer"
    @expose('/')
    def help(self):
        return self.response(200, message="Welcome to Colorizer API.")