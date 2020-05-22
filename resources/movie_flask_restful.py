from flask import Response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import (
    FieldDoesNotExist,
    NotUniqueError,
    DoesNotExist,
    ValidationError,
    InvalidQueryError,
)

from resources.errors import (
    SchemaValidationError,
    MovieAlreadyExistsError,
    InternalServerError,
    UpdatingMovieError,
    DeletingMovieError,
    MovieNotExistsError,
)
from database import Movie, User


class MoviesApi(Resource):
    def get(self):
        movies = Movie.objects.to_json()
        return Response(movies, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            body = request.get_json()
            movie = Movie.objects.create(**body, added_by=user)
            user.update(push__movies=movie)
            user.save()
            return {"id": str(movie.id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception:
            raise InternalServerError


class MovieApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            body = request.get_json()
            Movie.objects.get(id=id, added_by=user).update(**body)
            return "", 203
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            Movie.objects.get(id=id, added_by=user).delete()
            return "", 203
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            movie = Movie.objects.get(id=id).to_json()
            return Response(movie, mimetype="application/json", status=200)
        except DoesNotExist:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError
