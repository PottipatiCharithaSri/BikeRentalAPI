from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from Models.user import User
from Data.db import db
from Services.Interfaces.auth_interface import AuthInterface
from flask import current_app

class AuthService(AuthInterface):

    def login(self, data):
        user = User.query.filter_by(username=data["username"]).first()

        if not user:
            return None

        if not check_password_hash(user.password, data["password"]):
            return None

        return create_access_token(identity=user.id, additional_claims={"role": user.role})


    def register(self, data):
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user:
            return False

        user = User(
            username=data["username"],
            password=generate_password_hash(data["password"]),
            name=data["name"],
            age=data["age"],
            role="USER",
            
            aadhar=data.get("aadhar"),
            licence=data.get("licence")

        )

        db.session.add(user)
        db.session.commit()
        return True


auth_service = AuthService()