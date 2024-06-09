# create a model
from datetime import datetime
from QC import db

class YourModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(20), nullable=False)
    qc_status = db.Column(db.String(20), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"TrafficSystem(serial_number={self.serial_number}, qc_status={self.qc_status}, image_path={self.image_path}, date_added={self.date_added})"

        