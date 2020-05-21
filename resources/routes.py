from .movie_flask_restful import MovieApi, MoviesApi


def initialize_routes(api):
    api.add_resource(MoviesApi, "/api/movies")
    api.add_resource(MovieApi, "/api/movies/<id>")
