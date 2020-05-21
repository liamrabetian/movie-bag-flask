from flask import Blueprint, Response, request
from database import Movie


movies = Blueprint('movies', __name__)


@movies.route('/movies')
def get_movies() -> Response:
    movies = Movie.objects.to_json()
    return Response(movies, mimetype='application/json', status=200)


@movies.route('/movies/<id>')
def get_movie(id) -> Response:
    movies = Movie.objects.get(id=id).to_json()
    return Response(movies, mimetype='application/json', status=200)


@movies.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    movie = Movie.objects.create(**body)
    return {"id": str(movie.id)}, 200


@movies.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    body = request.get_json()
    Movie.objects.get(id=id).update(**body)
    return '', 200


@movies.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.objects.get(id=id).delete()
    return '', 200
