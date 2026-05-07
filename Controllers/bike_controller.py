from Data import db
from Models.bike import Bike
from Validators.bike_schema import BikeSchema
from Validators.validate_request import validate
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from Services.Service.bike_service import bike_service
from Auth.role_guard import admin_required
from flasgger import swag_from
bike_bp = Blueprint("bikes", __name__)

from flasgger import swag_from
from flask import request, jsonify

from flasgger import swag_from
from flask import request, jsonify

@bike_bp.before_request
@jwt_required()
def protect_bike_routes():
    pass

@swag_from({
    "tags": ["Bikes"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 1,
                        "description": "Bike ID (optional, usually auto-generated)"
                    },
                    "model": {
                        "type": "string",
                        "example": "Duke"
                    },
                    "available": {
                        "type": "boolean",
                        "example": True
                    }
                },
                "required": ["model", "available"]
            }
        }
    ],
    "responses": {
        201: {"description": "Bike added successfully"},
        401: {"description": "Login required"}
    }
})
@bike_bp.route("/bikes", methods=["POST"])
def add_bike():
    data = request.get_json()

    
    bike = Bike(
        model=data["model"],
        available=data["available"]
    )

    db.session.add(bike)
    db.session.commit()
    return {"message": "Bike added"}, 201
 


@bike_bp.route("/<int:bike_id>", methods=["GET"])
@jwt_required()
def get_bike(bike_id):
    """
    Get bike by ID
    ---
    tags:
      - Bikes
    security:
      - Bearer: []
    parameters:
      - in: path
        name: bike_id
        required: true
        type: integer
    responses:
      200:
        description: Bike found
      404:
        description: Bike not found
    """
    bike = bike_service.get_bike_by_id(bike_id)
    if not bike:
        return jsonify({"message": "Bike not found"}), 404
    return jsonify(bike), 200


@swag_from({
    "tags": ["Bikes"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "bike_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "example": 2
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "example": "Duke 390"
                    },
                    "available": {
                        "type": "boolean",
                        "example": False
                    }
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Bike updated successfully"},
        401: {"description": "Login required"},
        404: {"description": "Bike not found"}
    }
})
@bike_bp.route("/bikes/<int:bike_id>", methods=["PATCH"])
def update_bike(bike_id):
    data = request.get_json()
    bike = Bike.query.get(bike_id)
    if not bike:
        return jsonify({"message": "Bike not found"}), 404
    bike.model = data.get("model", bike.model)
    bike.available = data.get("available", bike.available)
    db.session.commit()
    return jsonify({"message": "Bike updated"}), 200
  
@bike_bp.route("/<int:bike_id>", methods=["DELETE"])
@jwt_required()
@admin_required()
def delete_bike(bike_id):
    """
    Delete a bike
    ---
    tags:
      - Bikes
    security:
      - Bearer: []
    parameters:
      - in: path
        name: bike_id
        required: true
        type: integer
    responses:
      200:
        description: Bike deleted
    """
    bike_service.delete_bike(bike_id)
    return jsonify({"message": "Bike deleted"}), 200