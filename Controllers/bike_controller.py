from Auth.role_guard import admin_required
from Data import db
from Models.bike import Bike
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from Models.enums.rental_status import RentalStatus
from Models.location import Location
from Models.rental import Rental
from flasgger import swag_from

bike_bp = Blueprint("bikes", __name__)

@swag_from({
    "tags": ["Bikes"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "query",
            "name": "location",
            "required": True,
            "type": "string",
            "example": "MG Road"
        }
    ],
    "responses": {
        200: {
            "description": "List of bikes",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "bike_id": {"type": "integer"},
                        "bike_model": {"type": "string"},
                        "location": {"type": "string"},
                        "available": {"type": "boolean"},
                        "expected_return_at": {
                            "type": "string",
                            "format": "date-time",
                            "nullable": True
                        }
                    }
                }
            }
        },
        404: {"description": "Location not found"}
    }
})
@bike_bp.route("", methods=["GET"])
@jwt_required()
def list_bikes_by_location():
    location_name = request.args.get("location")

    if not location_name:
        return jsonify({"message": "location query parameter is required"}), 400

    location = Location.query.filter_by(name=location_name).first()
    if not location:
        return jsonify({"message": "Location not found"}), 404

    bikes = Bike.query.filter_by(location_id=location.id).all()

    result = []
    for bike in bikes:
        rental = (
            Rental.query
            .filter(
                Rental.bike_id == bike.id,
                Rental.status.in_([
                    RentalStatus.RESERVED,
                    RentalStatus.ACTIVE,
                    RentalStatus.OVERDUE
                ])
            )
            .order_by(Rental.id.desc())
            .first()
        )

        result.append({
            "bike_id": bike.id,
            "bike_model": bike.model,
            "location": location.name,
            "available": rental is None,
            "expected_return_at": rental.expected_return_at if rental else None
        })

    return jsonify(result), 200


@swag_from({
    "tags": ["Bikes"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "example": "Activa 6G"
                    },
                    "location": {
                        "type": "string",
                        "example": "MG Road"
                    }
                },
                "required": ["model", "location"]
            }
        }
    ],
    "responses": {
        201: {"description": "Bike created successfully"},
        403: {"description": "Admin access required"},
        404: {"description": "Location not found"}
    }
})
@bike_bp.route("", methods=["POST"])
@jwt_required()
@admin_required()
def create_bike():
    data = request.get_json()

    if "model" not in data or "location" not in data:
        return jsonify({"error": "model and location are required"}), 400

    location = Location.query.filter_by(name=data["location"]).first()
    if not location:
        return jsonify({"error": "Location not found"}), 404

    bike = Bike(
        model=data["model"],
        location_id=location.id
    )

    db.session.add(bike)
    db.session.commit()

    return jsonify({
        "message": "Bike created successfully",
        "bike_id": bike.id,
        "model": bike.model,
        "location": location.name
    }), 201
