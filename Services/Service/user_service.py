from Models import user
from Models.user import User
from Data.db import db
from Services.Interfaces.user_interface import UserInterface


class UserService(UserInterface):

    def get_all_users(self):
        users = User.query.all()
        return [
            {
                "id": u.id,
                "name": u.name,
                "age": u.age
            }
            for u in users
        ]

    def get_user_by_id(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        return {
            "id": user.id,
            "name": user.name,
            "age": user.age
        }

    def create_user(self, data):
        user = User(
            name=data["name"],
            age=data["age"]
        )
        db.session.add(user)
        db.session.commit()

    def update_user(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None

        if "name" in data:
            user.name = data["name"]

        if "age" in data:
            user.age = data["age"]

        db.session.commit()
        return user
    
    def delete_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return False

        db.session.delete(user)
        db.session.commit()
        return True


user_service = UserService()