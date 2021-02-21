import sqlite3
from flask_jwt import jwt_required
from models.vitals import Patient_info


class from_db_to_api(Patient_info):
    @jwt_required()
    def post(self, patient_id):
        patient_vitals = Patient_info.health_info.parse_args()
        Patient_info.insert(patient_id, patient_vitals)
        return "Information has been added successfully"

    def get(self, patient_id):
        vitals = Patient_info.find_by_id(patient_id)
        if vitals:
            return vitals
        else:
            return "Patient that you are searching does not exist"

    # delete function deletes last entry of vital signs to undo invalid data entry
    @jwt_required()
    def delete(self, patient_id):
        connection = sqlite3.connect("Health_data.db")
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Health_info WHERE row_id = '
                       '(SELECT MAX(row_id) From Health_info WHERE patient_id =?)', (patient_id,))
        connection.commit()
        connection.close()
        return "Last entry has been deleted"

    # put function only changes last entry of vital signs
    @jwt_required()
    def put(self, patient_id):
        patient_vitals = Patient_info.health_info.parse_args()
        connection = sqlite3.connect("Health_data.db")
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM Health_info WHERE row_id = (SELECT MAX(row_id) From Health_info WHERE patient_id =?)',
            (patient_id,))
        value = cursor.fetchone()
        if value:
            Patient_info.update(patient_id, patient_vitals)
            return "last entry has been updated"
        else:
            Patient_info.insert(patient_id, patient_vitals)
        connection.commit()
        connection.close()
        return "Information has been added successfully"
