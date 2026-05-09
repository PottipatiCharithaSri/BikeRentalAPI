from Data.db import db
from datetime import datetime
class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey("bikes.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    user = db.relationship("User", backref="rentals")
    bike = db.relationship("Bike", backref="rentals")

    expected_return_at = db.Column(db.DateTime, nullable=True)