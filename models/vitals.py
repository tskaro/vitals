from flask import jsonify
from flask_restful import Resource, reqparse
import time
import sqlite3

# Creating database for the project
connection = sqlite3.connect("Health_data.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Health_info (row_id INTEGER PRIMARY KEY, patient_id integer, "
               "Glucose integer, SBP integer, DBP integer, time str)")
connection.commit()
connection.close()

# Makes dictionary from row for representing
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Full_data(Resource):
    def get(self):
        connection = sqlite3.connect("Health_data.db")
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Health_info')
        patient_data = cursor.fetchall()
        connection.commit()
        connection.close()
        return jsonify(patient_data)


class Patient_info(Resource):
    health_info = reqparse.RequestParser()
    health_info.add_argument("Glucose", type=int, required=True, help="Enter your latest blood glucose reading")
    health_info.add_argument("SBP", type=int, required=False)  # სისტოლური წნევა _ წნევა როცა გული შეიკუმშა
    health_info.add_argument("DBP", type=int, required=False)  # დიასტოლური წნევა _ წნევა როცა გული მოდუნდა

    @classmethod
    def insert(cls, patient_id, Hinfo):
        connection = sqlite3.connect("Health_data.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Health_info(patient_id, Glucose, SBP, DBP, time) VALUES(?,?,?,?,?)', (
            patient_id, Hinfo["Glucose"], Hinfo["SBP"], Hinfo["DBP"], time.strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()
        connection.close()

    @classmethod
    def find_by_id(cls, patient_id):
        connection = sqlite3.connect("Health_data.db")
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Health_info WHERE patient_id = ?', (patient_id,))
        vitals = cursor.fetchall()
        print(vitals)
        connection.commit()
        connection.close()
        if vitals:
            return vitals

    @classmethod
    def update(cls, patient_id, Hinfo):
        connection = sqlite3.connect("Health_data.db")
        cursor = connection.cursor()
        cursor.execute('UPDATE Health_info SET Glucose=?, SBP=?, DBP=?, time=? '
                       'WHERE row_id = (SELECT MAX(row_id) From Health_info WHERE patient_id =?)',
                       (Hinfo["Glucose"], Hinfo["SBP"], Hinfo["DBP"],
                        time.strftime('%Y-%m-%d %H:%M:%S'), patient_id))
        connection.commit()
        connection.close()

