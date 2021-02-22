from flask_restful import reqparse
from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    create_user_parser = reqparse.RequestParser()
    create_user_parser.add_argument("id", help="Enter your id")
    create_user_parser.add_argument("username", required=True, help="Enter your username")
    create_user_parser.add_argument("password", required=True, help="Enter your password")

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
