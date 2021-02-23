from flask import Flask, redirect
from flask_restful import Api
from resources.vitals import from_db_to_api
from resources.users import User_registration
from flask_jwt import JWT
from security import authentication, identity

app = Flask(__name__)
app.secret_key = "unbelievable_secret_key"
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Health_data.db'

api = Api(app)
jwt = JWT(app, authentication, identity)


@app.route("/")
def home():
    return redirect("https://github.com/tskaro/vitals")


api.add_resource(from_db_to_api, '/vitals/<int:patient_id>')
api.add_resource(User_registration, '/registration')

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    app.run(debug=True, port=500)
