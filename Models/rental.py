from Data.db import db
from datetime import datetime, timezone

from Models.enums.cancellation_reason import CancellationReason
from Models.enums.duration_unit import DurationUnit
from Models.enums.rental_status import RentalStatus
from Models.enums.return_reason import ReturnReason
class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey("bikes.id"), nullable=False)
    status = db.Column(db.Enum(RentalStatus), nullable=False)
    
    reserved_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    rental_start_time = db.Column(db.DateTime(timezone=True))
    expected_return_at = db.Column(db.DateTime(timezone=True))
    actual_return_time = db.Column(db.DateTime(timezone=True))
    cancelled_at = db.Column(db.DateTime(timezone=True))

    duration_value = db.Column(db.Integer)
    duration_unit = db.Column(db.Enum(DurationUnit))

    return_reason = db.Column(db.Enum(ReturnReason))
    cancellation_reason = db.Column(db.Enum(CancellationReason))
