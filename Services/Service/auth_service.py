from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from Models.user import User
from Data.db import db
from Services.Interfaces.auth_interface import AuthInterface
from flask import current_app

class AuthService(AuthInterface):

    def register(self, data):
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user:
            return None

        user = User(
            username=data["username"],
            password=generate_password_hash(data["password"]),
            name=data["name"],
            age=data["age"],            
            aadhar=data.get("aadhar"),
            licence=data.get("licence"),
            role="user"
        )

        db.session.add(user)
        db.session.commit()
        return user


auth_service = AuthService()