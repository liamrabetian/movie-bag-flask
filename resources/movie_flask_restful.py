from flask import Response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import Movie, User


class MoviesApi(Resource):
    def get(self):
        movies = Movie.objects.to_json()
        return Response(movies, mimetype='application/json', status=200)
    
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        body = request.get_json()
        movie = Movie.objects.create(**body, added_by=user)
        user.update(push__movies=movie)
        user.save()
        return {'id': str(movie.id)}, 200


class MovieApi(Resource):

    @jwt_required
    def put(self, id):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        body = request.get_json()
        Movie.objects.get(id=id, added_by=user).update(**body)
        return '', 203
    
    @jwt_required
    def delete(self, id):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        Movie.objects.get(id=id, added_by=user).delete()
        return '', 203
    
    def get(self, id):
        movie = Movie.objects.get(id=id).to_json()
        return Response(movie, mimetype='application/json', status=200)
