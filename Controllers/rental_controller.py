from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from Services.Service.rental_service import rental_service
from flasgger import swag_from
from Models.bike import Bike

from Validators.rental_schema import RentBikeSchema
from Validators.validate_request import validate

rental_bp = Blueprint("rentals", __name__)


@rental_bp.route("/rent/<int:rental_id>", methods=["GET"])
@jwt_required()
def get_rental(rental_id):
    """
    Get rental by ID
    ---
    tags:
      - Rentals
    security:
      - Bearer: []
    parameters:
      - in: path
        name: rental_id
        required: true
        type: integer
    responses:
      200:
        description: Rental found
      404:
        description: Rental not found
    """
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
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "bike_id": {"type": "integer", "example": 1}
                },
                "required": ["bike_id"]
            }
        }
    ],
    "responses": {
        201: {"description": "Bike rented"},
        400: {"description": "Bike not available"}
    }
})
@rental_bp.route("/rent", methods=["POST"])
@jwt_required()
@validate(RentBikeSchema)
def rent_bike():
    from Models.location import Location
    from Models.rental import Rental
    from datetime import datetime, timedelta
    from Data.db import db

    user_id = int(get_jwt_identity())

    location_name = request.json["location"]

    location = Location.query.filter_by(name=location_name).first()
    if not location:
        return jsonify({"message": "Location not found"}), 404

    bike = Bike.query.filter_by(
        location_id=location.id,
        available=True
    ).first()

    if not bike:
        return jsonify({"message": "No bikes available at this location"}), 400

    rental = Rental(
        user_id=user_id,
        bike_id=bike.id,
        status="RENTED",
        expected_return_at=datetime.utcnow() + timedelta(hours=24)
    )

    bike.available = False
    bike.user_id = user_id

    db.session.add(rental)
    db.session.commit()

    return jsonify({
        "message": "Bike rented successfully",
        "bike_model": bike.model,
        "location": location.name,
        "expected_return_at": rental.expected_return_at
    }), 201


@rental_bp.route("/rent/<int:rental_id>", methods=["PATCH"])
@jwt_required()
def return_rental(rental_id):
    """
    Return rented bike
    ---
    tags:
      - Rentals
    security:
      - Bearer: []
    parameters:
      - in: path
        name: rental_id
        required: true
        type: integer
    responses:
      200:
        description: Bike returned
      404:
        description: Rental not found
    """
    
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return {"message": "Rental not found"}, 404

    current_user_id = int(get_jwt_identity())
    role = get_jwt().get("role")

    if rental["user_id"] != current_user_id and role != "admin":
        return {"message": "Access denied"}, 403

    success, message = rental_service.return_bike(rental_id)
    return jsonify({"message": message}), 200



@rental_bp.route("/rent/<int:rental_id>", methods=["DELETE"])
@jwt_required()
def cancel_rental(rental_id):
    """
    Cancel rental
    ---
    tags:
      - Rentals
    security:
      - Bearer: []
    parameters:
      - in: path
        name: rental_id
        required: true
        type: integer
    responses:
      200:
        description: Rental cancelled
      404:
        description: Rental not found
    """
    
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return {"message": "Rental not found"}, 404

    current_user_id = int(get_jwt_identity())
    role = get_jwt().get("role")

    if rental["user_id"] != current_user_id and role != "admin":
        return {"message": "Access denied"}, 403

    success, message = rental_service.cancel_rental(rental_id)
    return jsonify({"message": message}), 200
