from Models.rental import Rental
from Models.bike import Bike
from Data.db import db
from Services.Interfaces.rental_interface import RentalInterface


class RentalService(RentalInterface):

    def get_all_rentals(self):
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "bike_id": r.bike_id,
                "status": r.status
            }
            for r in Rental.query.all()
        ]

    def get_rental_by_id(self, rental_id):
        rental = Rental.query.get(rental_id)
        if not rental:
            return None

        return {
            "id": rental.id,
            "user_id": rental.user_id,
            "bike_id": rental.bike_id,
            "status": rental.status
        }

    def create_rental(self, user_id, bike_id):
        bike = Bike.query.get(bike_id)
        if not bike or not bike.available:
            return False, "Bike not available"

        rental = Rental(
            user_id=user_id,
            bike_id=bike_id,
            status="RENTED"
        )

        bike.available = False
        db.session.add(rental)
        db.session.commit()

        return True, "Bike rented successfully"

    def return_bike(self, rental_id):
        rental = Rental.query.get(rental_id)
        if not rental or rental.status != "RENTED":
            return False, "Rental not found"

        bike = Bike.query.get(rental.bike_id)
        if bike:
            bike.available = True

        rental.status = "RETURNED"
        db.session.commit()

        return True, "Bike returned"

    def cancel_rental(self, rental_id):
        rental = Rental.query.get(rental_id)
        if not rental:
            return False, "Rental not found"

        bike = Bike.query.get(rental.bike_id)
        if bike:
            bike.available = True

        rental.status = "CANCELLED"
        db.session.commit()

        return True, "Rental cancelled"


rental_service = RentalService()