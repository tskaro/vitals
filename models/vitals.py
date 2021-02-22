from flask_restful import reqparse
from db import db


class Patient_info(db.Model):
    __tablename__ = "Health_info"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    Glucose = db.Column(db.Integer)
    SBP = db.Column(db.Integer)
    DBP = db.Column(db.Integer)
    time = db.Column(db.String)

    def __init__(self, patient_id, Glucose, SBP, DBP, time):
        self.patient_id = patient_id
        self.Glucose = Glucose
        self.SBP = SBP
        self.DBP = DBP
        self.time = time

    health_info = reqparse.RequestParser()
    health_info.add_argument("Glucose", type=int, required=True, help="Enter your latest blood glucose reading")
    health_info.add_argument("SBP", type=int, required=False)  # სისტოლური წნევა _ წნევა როცა გული შეიკუმშა
    health_info.add_argument("DBP", type=int, required=False)  # დიასტოლური წნევა _ წნევა როცა გული მოდუნდა

    def json(self):
        return {"patient_id": self.patient_id, "Glucose": self.Glucose,
                "SBP": self.SBP, "DBP": self.DBP, "time": self.time}

    @classmethod
    def find_by_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).all()

    @classmethod
    def last_entry(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).order_by(cls.row_id.desc()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
