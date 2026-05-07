from Models import bike
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
        
    def create_bike(self, data):
        bike = Bike(
            model=data["model"],
            available=True
        )
        db.session.add(bike)
        db.session.commit()


bike_service = BikeService()