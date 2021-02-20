import sqlite3
from flask_restful import reqparse


class User:
    create_user_parser = reqparse.RequestParser()
    create_user_parser.add_argument("username", required=True, help="Enter your username")
    create_user_parser.add_argument("password", required=True, help="Enter your password")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('Health_Data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        row = cursor.fetchone()
        connection.commit()
        connection.close()
        if row:
            return cls(*row)

    @classmethod
    def find_by_id(cls, user_id):
        connection = sqlite3.connect('Health_Data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        row = cursor.fetchone()
        connection.commit()
        connection.close()
        if row:
            return cls(*row)

    @classmethod
    def add(cls, new_user):
        user_existence = User.find_by_username(new_user.get('username'))
        if user_existence:
            return "User already exists"
        connection = sqlite3.connect('Health_Data.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users(username, password) VALUES(?,?)',
                       (new_user["username"], new_user["password"]))
        connection.commit()
        connection.close()
        return "New user has been added"
