from Data.db import db
from Models.location import Location

class Bike(db.Model):
    __tablename__ = "bikes"

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)

    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    location = db.relationship("Location", backref="bikes")

