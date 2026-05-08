from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Auth.role_guard import admin_required
from Data.db import db
from Models.location import Location
from Validators.location_schema import LocationSchema
from Validators.validate_request import validate

location_bp = Blueprint("locations", __name__)

@location_bp.route("/locations", methods=["POST"])
@jwt_required()
@admin_required()
@validate(LocationSchema)
def create_location():
    data = request.get_json()

    location = Location(
        name=data["name"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )

    db.session.add(location)
    db.session.commit()

    return jsonify({"message": "Location created"}), 201


@location_bp.route("/locations", methods=["GET"])
@jwt_required()
def get_locations():
    locations = Location.query.all()
    return jsonify([
        {
            "id": l.id,
            "name": l.name,
            "latitude": l.latitude,
            "longitude": l.longitude
        }
        for l in locations
    ])