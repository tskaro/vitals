from flask import Flask
from flask_restful import Api
from models.vitals import Full_data
from resources.vitals import from_db_to_api
from resources.users import User_registration

app = Flask(__name__)
api = Api(app)

api.add_resource(Full_data, '/vitals/')
api.add_resource(from_db_to_api, '/vitals/<int:patient_id>')
api.add_resource(User_registration, '/registration')
if __name__ == '__main__':
    app.run(debug=True, port=500)
