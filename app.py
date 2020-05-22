from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from database import initialize_db
from resources import movies
from resources.errors import errors


app = Flask(__name__)


app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

app.config.from_envvar('ENV_FILE_LOCATION')

mail = Mail(app)
# imports requiring app and mail
from resources.routes import initialize_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)

app.register_blueprint(movies)

initialize_routes(api)

app.run()
