from Models.bike import Bike
from Data.db import db
from Services.Interfaces.bike_interface import BikeInterface

class BikeService(BikeInterface):

    def get_all_bikes(self):
        bikes = Bike.query.all()
        return [
            {
                "id": b.id,
                "model": b.model,
                "available": b.available
            }
            for b in bikes
        ]

    def get_bike_by_id(self, bike_id):
        bike = Bike.query.get(bike_id)
        if not bike:
            return None
        return {
            "id": bike.id,
            "model": bike.model
        }

bike_service = BikeService()