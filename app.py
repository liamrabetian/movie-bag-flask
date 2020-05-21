from flask import Flask
from flask_restful import Api

from database import initialize_db
from resources import movies
from resources.routes import initialize_routes


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

initialize_db(app)

app.register_blueprint(movies)

api = Api(app)
initialize_routes(api)

app.run()
