from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from Services.Service.rental_service import rental_service
from flasgger import swag_from

from Validators.rental_schema import (
    RentBikeSchema,
    ReturnRentalSchema,
    CancelRentalSchema
)
from Validators.validate_request import validate

rental_bp = Blueprint("rentals", __name__)


@swag_from({
    "tags": ["Rentals"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "path",
            "name": "rental_id",
            "required": True,
            "type": "integer"
        }
    ],
    "responses": {
        200: {"description": "Rental found"},
        403: {"description": "Access denied"},
        404: {"description": "Rental not found"}
    }
})
@rental_bp.route("/rent/<int:rental_id>", methods=["GET"])
@jwt_required()
def get_rental(rental_id):
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return jsonify({"message": "Rental not found"}), 404

    current_user_id = int(get_jwt_identity())
    role = get_jwt().get("role")

    if rental["user_id"] != current_user_id and role != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify(rental), 200


@swag_from({
    "tags": ["Rentals"],
    "security": [{"Bearer": []}],
    "responses": {
        200: {"description": "List of user rentals"}
    }
})
@rental_bp.route("/rent/my", methods=["GET"])
@jwt_required()
def get_my_rentals():
    user_id = int(get_jwt_identity())
    rentals = rental_service.get_rentals_by_user(user_id)
    return jsonify(rentals), 200


@swag_from({
    "tags": ["Rentals"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "bike_id": {"type": "integer", "example": 1},
                    "duration_value": {"type": "integer", "example": 2},
                    "duration_unit": {"type": "string", "example": "HOURS"}
                },
                "required": ["bike_id", "duration_value", "duration_unit"]
            }
        }
    ],
    "responses": {
        201: {"description": "Bike reserved"},
        400: {"description": "Bike not available"}
    }
})
@rental_bp.route("/rent/reserve", methods=["POST"])
@jwt_required()
@validate(RentBikeSchema)
def reserve_rental():
    user_id = int(get_jwt_identity())
    data = request.json

    success, rental_id, message = rental_service.reserve_rental(
        user_id,
        data["bike_id"],
        data["duration_value"],
        data["duration_unit"]
    )
    
    if not success:
      return jsonify({"message": message}), 400

    
    return jsonify({
        "message": message,
        "rental_id": rental_id
    }), 201




@swag_from({
    "tags": ["Rentals"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "path",
            "name": "rental_id",
            "required": True,
            "type": "integer",
            "example": 5
        }
    ],
    "responses": {
        200: {"description": "Rental started"},
        400: {"description": "Invalid state"},
        404: {"description": "Rental not found"}
    }
})
@rental_bp.route("/rent/<int:rental_id>/start", methods=["PATCH"])
@jwt_required()
def start_rental(rental_id):
    success, message = rental_service.start_rental(rental_id)
    return jsonify({"message": message}), 200 if success else 400


@swag_from({
    "tags": ["Rentals"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "path",
            "name": "rental_id",
            "required": True,
            "type": "integer",
            "example": 5
        },
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "return_reason": {
                        "type": "string",
                        "example": "COMPLETED"
                    }
                },
                "required": ["return_reason"]
            }
        }
    ],
    "responses": {
        200: {"description": "Bike returned"},
        400: {"description": "Invalid state"},
        403: {"description": "Access denied"},
        404: {"description": "Rental not found"}
    }
})
@rental_bp.route("/rent/<int:rental_id>", methods=["PATCH"])
@jwt_required()
@validate(ReturnRentalSchema)
def return_rental(rental_id):
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return jsonify({"message": "Rental not found"}), 404

    current_user_id = int(get_jwt_identity())
    role = get_jwt().get("role")

    if rental["user_id"] != current_user_id and role != "admin":
        return jsonify({"message": "Access denied"}), 403

    success, message = rental_service.return_bike(
        rental_id,
        request.json["return_reason"]
    )

    return jsonify({"message": message}), 200 if success else 400


@swag_from({
    "tags": ["Rentals"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "path",
            "name": "rental_id",
            "required": True,
            "type": "integer",
            "example": 2
        },
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "cancellation_reason": {
                        "type": "string",
                        "example": "CUSTOMER_CHANGED_MIND"
                    }
                },
                "required": ["cancellation_reason"]
            }
        }
    ],
    "responses": {
        200: {"description": "Rental cancelled"},
        400: {"description": "Invalid state"},
        403: {"description": "Access denied"},
        404: {"description": "Rental not found"}
    }
})
@rental_bp.route("/rent/<int:rental_id>", methods=["DELETE"])
@jwt_required()
@validate(CancelRentalSchema)
def cancel_rental(rental_id):
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return jsonify({"message": "Rental not found"}), 404

    current_user_id = int(get_jwt_identity())
    role = get_jwt().get("role")

    if rental["user_id"] != current_user_id and role != "admin":
        return jsonify({"message": "Access denied"}), 403

    success, message = rental_service.cancel_rental(
        rental_id,
        request.json["cancellation_reason"]
    )

    return jsonify({"message": message}), 200 if success else 400


@swag_from({
    "tags": ["Rentals"],
    "security": [{"Bearer": []}],
    "responses": {
        200: {"description": "Overdue rentals updated"},
        403: {"description": "Admin access required"}
    }
})
@rental_bp.route("/rent/overdue/check", methods=["POST"])
@jwt_required()
def mark_overdue():
    role = get_jwt().get("role")
    if role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    count = rental_service.mark_overdue_rentals()
    return jsonify({"message": f"{count} rental(s) marked as OVERDUE"}), 200