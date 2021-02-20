from flask_restful import Resource
from models.users import User


class User_registration(Resource):

    def post(self):
        new_user = User.create_user_parser.parse_args()
        return User.add(new_user)
