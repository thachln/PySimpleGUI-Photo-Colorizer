from flask import Flask
from flask_appbuilder import SQLA, AppBuilder

from api.colorizer_api import ColorizerApi

if __name__ == '__main__':
    app = Flask(__name__)
    db = SQLA(app)

    appbuilder = AppBuilder(app, db.session)

    # Add classes of API
    appbuilder.add_api(ColorizerApi)

    print('Try to open URL http://127.0.0.1:5000/api/colorizer')
    app.run(host='localhost', port=5000)



