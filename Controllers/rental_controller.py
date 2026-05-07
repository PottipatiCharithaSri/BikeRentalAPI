from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from Services.Service.rental_service import rental_service
from flasgger import swag_from

rental_bp = Blueprint("rentals", __name__)


@rental_bp.before_request
@jwt_required()
def protect_rental_routes():
    pass


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
def rent_bike():
    data = request.get_json()
    bike_id = data["bike_id"]

    success, message = rental_service.create_rental(
        user_id=get_jwt_identity(),
        bike_id=bike_id
    )

    return jsonify({"message": message}), 201 if success else 400


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

    # ✅ Owner or admin only
    if rental["user_id"] != current_user_id and role != "ADMIN":
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

    if rental["user_id"] != current_user_id and role != "ADMIN":
        return {"message": "Access denied"}, 403

    success, message = rental_service.cancel_rental(rental_id)
    return jsonify({"message": message}), 200
