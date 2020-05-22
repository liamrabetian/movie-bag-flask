from flask_bcrypt import check_password_hash, generate_password_hash

from .db import db


class Movie(db.Document):
    name = db.StringField(required=True, unique=True)
    casts = db.ListField(db.StringField(), required=True)
    genres = db.ListField(db.StringField(), required=True)
    added_by = db.RefrenceField('User')


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    movies = db.ListField(db.RefrenceField('Movie', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
User.register_delete_rule(Movie, 'added_by', db.CASCADE)
