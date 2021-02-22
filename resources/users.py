from flask_restful import Resource
from models.users import User


class User_registration(Resource):

    def post(self):
        new_user = User.create_user_parser.parse_args()
        user_existence = User.find_by_username(new_user.get('username'))
        if user_existence:
            return "User already exists"
        User(**new_user).save_to_db()
        return "New user has been added"
