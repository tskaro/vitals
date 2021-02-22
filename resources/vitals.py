import time
from flask_jwt import jwt_required
from models.vitals import Patient_info
from flask_restful import Resource


class from_db_to_api(Resource):

    @jwt_required()
    def post(self, patient_id):
        patient_vitals = Patient_info.health_info.parse_args()
        data = Patient_info(patient_id, patient_vitals['Glucose'], patient_vitals['SBP'],
                            patient_vitals['DBP'], time.strftime('%Y-%m-%d %H:%M:%S'))
        data.save_to_db()
        return "Information has been added successfully"

    def get(self, patient_id):
        vitals = Patient_info.find_by_id(patient_id)
        if vitals:
            jsons = []
            for vital in vitals:
                jsons.append(vital.json())
            return jsons
        else:
            return "Patient that you are searching does not exist"

    # delete function deletes last entry of vital signs to undo invalid data entry
    @jwt_required()
    def delete(self, patient_id):
        vitals = Patient_info.find_by_id(patient_id)
        if vitals:
            item = Patient_info.last_entry(patient_id)
            item.delete_from_db()
            return "Entry has been deleted successfully"
        else:
            return f"Patient with id: {patient_id} does not exist"

    # put function only changes last entry of vital signs
    @jwt_required()
    def put(self, patient_id):
        patient_vitals = Patient_info.health_info.parse_args()
        item = Patient_info.last_entry(patient_id)

        if item:
            item.Glucose = patient_vitals['Glucose']
            item.sbp = patient_vitals['SBP']
            item.DBP = patient_vitals['DBP']
            item.time = time.strftime('%Y-%m-%d %H:%M:%S')
            message = "Correction has been made"
        else:
            item = Patient_info(patient_id, patient_vitals['Glucose'], patient_vitals['SBP'],
                                patient_vitals['DBP'], time.strftime('%Y-%m-%d %H:%M:%S'))
            message = "new patients info has been added"

        item.save_to_db()
        return message, item.json()
