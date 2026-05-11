from Models.rental import Rental
from Models.bike import Bike
from Data.db import db
from Services.Interfaces.rental_interface import RentalInterface

from datetime import datetime, timedelta, timezone

from Models.enums.rental_status import RentalStatus
from Models.enums.duration_unit import DurationUnit
from Models.enums.return_reason import ReturnReason
from Models.enums.cancellation_reason import CancellationReason


class RentalService(RentalInterface):

    def reserve_rental(self, user_id, bike_id, duration_value, duration_unit):
        bike = Bike.query.get(bike_id)
        if not bike or not bike.available:
            return False, None, "Bike not available"

        now = datetime.now(timezone.utc)
        expected_return_at = self._calculate_return_time(
            now, duration_value, duration_unit
        )

        rental = Rental(
            user_id=user_id,
            bike_id=bike_id,
            status=RentalStatus.RESERVED,
            reserved_at=now,
            duration_value=duration_value,
            duration_unit=DurationUnit(duration_unit),
            expected_return_at=expected_return_at
        )

        bike.available = False
        db.session.add(rental)
        db.session.commit()

        return True, rental.id, "Bike reserved successfully"
    
    
    def get_rentals_by_user(self, user_id):
        rentals = (
            Rental.query
            .filter(Rental.user_id == user_id)
            .order_by(Rental.id.desc())
            .all()
        )

        return [
            {
                "rental_id": r.id,
                "bike_id": r.bike_id,
                "status": r.status.value,
                "expected_return_at": r.expected_return_at
            }
            for r in rentals
        ]

    def get_rental_by_id(self, rental_id):
        rental = Rental.query.get(rental_id)
        if not rental:
            return None

        return {
            "rental_id": rental.id,
            "user_id": rental.user_id,
            "bike_id": rental.bike_id,
            "status": rental.status.value,
            "expected_return_at": rental.expected_return_at
        }
        
    def start_rental(self, rental_id):
        rental = Rental.query.get(rental_id)
        if not rental or rental.status != RentalStatus.RESERVED:
            return False, "Rental cannot be started"

        rental.status = RentalStatus.ACTIVE
        rental.rental_start_time = datetime.now(timezone.utc)
        db.session.commit()

        return True, "Rental started"

    def return_bike(self, rental_id, return_reason):
        rental = Rental.query.get(rental_id)
        if not rental or rental.status != RentalStatus.ACTIVE:
            return False, "Rental not active"

        rental.status = RentalStatus.RETURNED
        rental.actual_return_time = datetime.now(timezone.utc)
        rental.return_reason = ReturnReason(return_reason)
        bike = Bike.query.get(rental.bike_id)
        bike.available = True

        db.session.commit()

        return True, "Bike returned successfully"

    def cancel_rental(self, rental_id, cancellation_reason):
        rental = Rental.query.get(rental_id)
        if not rental or rental.status != RentalStatus.RESERVED:
            return False, "Only reserved rentals can be cancelled"

        rental.status = RentalStatus.CANCELLED
        rental.cancelled_at = datetime.now(timezone.utc)
        rental.cancellation_reason = CancellationReason(cancellation_reason)
        bike = Bike.query.get(rental.bike_id)
        bike.available = True

        db.session.commit()

        return True, "Rental cancelled"

    def _calculate_return_time(self, start_time, value, unit):
        if unit == "HOURS":
            return start_time + timedelta(hours=value)
        if unit == "DAYS":
            return start_time + timedelta(days=value)
        if unit == "WEEKS":
            return start_time + timedelta(weeks=value)
        raise ValueError("Invalid duration unit")

    def mark_overdue_rentals(self):
        now = datetime.now(timezone.utc)

        overdue_rentals = (
            Rental.query
            .filter(
                Rental.status == RentalStatus.ACTIVE,
                Rental.expected_return_at < now
            )
            .all()
        )

        for rental in overdue_rentals:
            rental.status = RentalStatus.OVERDUE

        if overdue_rentals:
            db.session.commit()

        return len(overdue_rentals)


rental_service = RentalService()