from Data.db import db

class User(db.Model):
    __tablename__ = "users"

    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    role = db.Column(db.String(20), default="USER")
    
    aadhar = db.Column(db.String(20), nullable=True)
    licence = db.Column(db.String(30), nullable=True)
