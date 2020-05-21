from flask_bcrypt import check_password_hash, generate_password_hash

from .db import db


class Movie(db.Document):
    name = db.StringField(required=True, unique=True)
    casts = db.ListField(db.StringField(), required=True)
    genres = db.ListField(db.StringField(), required=True)


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
