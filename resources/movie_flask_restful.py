from flask import Response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required

from database import Movie


class MoviesApi(Resource):
    def get(self):
        movies = Movie.objects.to_json()
        return Response(movies, mimetype='application/json', status=200)
    
    @jwt_required
    def post(self):
        body = request.get_json()
        movie = Movie.objects.create(**body)
        return {'id': str(movie.id)}, 200


class MovieApi(Resource):

    @jwt_required
    def put(self, id):
        body = request.get_json()
        Movie.objects.get(id=id).update(**body)
        return '', 203
    
    @jwt_required
    def delete(self, id):
        Movie.objects.get(id=id).delete()
        return '', 203
    
    def get(self, id):
        movie = Movie.objects.get(id=id).to_json()
        return Response(movie, mimetype='application/json', status=200)
