from Data import db
from Models.bike import Bike
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from Services.Service.bike_service import bike_service
bike_bp = Blueprint("bikes", __name__)
import math

def distance_km(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111

@bike_bp.route("/by-location/<int:location_id>", methods=["GET"])
@jwt_required()
def get_bikes_by_location(location_id):
    bikes = Bike.query.filter_by(
        location_id=location_id,
        available=True
    ).all()

    return jsonify([
        {
            "id": b.id,
            "model": b.model,
            "location_id": b.location_id
        }
        for b in bikes
    ]), 200


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