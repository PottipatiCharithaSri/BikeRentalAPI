from Models import user
from Models.user import User
from Validators.auth_schema import LoginSchema, RegisterSchema
from Validators.validate_request import validate
from flask import Blueprint, request, jsonify
from Services.Service.auth_service import auth_service
from flasgger import swag_from
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from Data.db import jwt_blocklist
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

@swag_from({
    "tags": ["Auth"],
    "security": [],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "example": "Charitha"
                    },
                    "password": {
                        "type": "string",
                        "example": "Charitha123"
                    }
                },
                "required": ["username", "password"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "JWT token returned"
        },
        401: {
            "description": "Invalid credentials"
        }
    }
})
@auth_bp.route("/login", methods=["POST"])
@validate(LoginSchema)
def login():
  
    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    
    if not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    
    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "access_token": access_token
    }), 200



@swag_from({
    "tags": ["Auth"],
    "summary": "Register a new user",
    "description": (
        "Register a new user.\n\n"
        "⚠️ Either **Aadhaar number** OR **Driving Licence number** is required.\n\n"
        "✅ **Important:** Save the returned `user_id`. "
            "You will need this `user_id` for **all future operations** "
            "(renting a bike, updating details, or any other actions).\n\n"
            "- Aadhaar must be 12 digits and not start with 0 or 1\n"
            "- Licence must follow Indian DL format (e.g. KA0120190001234)"
        ),
    
    "security": [],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["username", "password", "name", "age"],
                "properties": {
                    "username": {
                        "type": "string",
                        "example": "rishaan19"
                    },
                    "password": {
                        "type": "string",
                        "example": "Rishaan@123"
                    },
                    "name": {
                        "type": "string",
                        "example": "Rishaan"
                    },
                    "age": {
                        "type": "integer",
                        "example": 19
                    },
                    "aadhar": {
                        "type": "string",
                        "example": "234567890123",
                        "description": "Required if licence is not provided"
                    },
                    "licence": {
                        "type": "string",
                        "example": "KA0120190001234",
                        "description": "Required if aadhar is not provided"
                    }
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "User registered successfully. The response will contain the generated user_id."
        },
        400: {
            "description": "Validation error"
        }
    }
})
@auth_bp.route("/register", methods=["POST"])
@validate(RegisterSchema)
def register():
    user = auth_service.register(request.json)

    if not user:
        return jsonify({"error": "Username already exists"}), 400

    return jsonify({
    "message": "User registered",
    "user_id": user.id
}), 201


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout user
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Successfully logged out
    """
    jti = get_jwt()["jti"]
    jwt_blocklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200
