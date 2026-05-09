from Validators.user_schema import UpdateUserSchema
from Validators.validate_request import validate
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from Services.Service.user_service import user_service
from flasgger import swag_from

user_bp = Blueprint("users", __name__)


@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        required: true
        type: integer
    responses:
      200:
        description: User found
      404:
        description: User not found
    """
    
    current_user_id = int(get_jwt_identity())
    role = get_jwt().get("role")

    if current_user_id != user_id and role != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user), 200
  

@swag_from({
    "tags": ["Users"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "type": "integer"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Cherry"                   
                    },
                    "age": {
                        "type": "integer",
                        "example": 28
                    }
                }
            }
        }
    ],
    "responses": {
        200: {"description": "User updated"},
        404: {"description": "User not found"}
    }
})
@user_bp.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
@validate(UpdateUserSchema)
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    role = get_jwt().get("role")

    if current_user_id == user_id:
        user_service.update_user(user_id, request.json)
        return jsonify({"message": "Profile updated"}), 200

    if role == "ADMIN":
        user_service.update_user(user_id, request.json)
        return jsonify({"message": "User updated by admin"}), 200

    return jsonify({"message": "You are not allowed to update this user"}), 403


  
@swag_from({
    "tags": ["Users"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "example": 2
        }
    ],
    "responses": {
        200: {"description": "User deleted"},
        404: {"description": "User not found"}
    }
})
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    
    role = get_jwt().get("role")

    if role != "ADMIN":
        return jsonify({"message": "Only admin can delete users"}), 403

    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"message": "User deleted"}), 200

