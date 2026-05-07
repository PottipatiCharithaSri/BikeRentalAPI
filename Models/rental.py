from Data.db import db
class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey("bikes.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)