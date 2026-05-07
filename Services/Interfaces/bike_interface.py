from typing import List, Dict

class BikeInterface:
    def get_all_bikes(self) -> List:
        """
        Fetch all bikes.
        Returns a list of bike dictionaries.
        """
        raise NotImplementedError

    def create_bike(self, data: Dict) -> None:
        """
        Create a new bike.
        """
        raise NotImplementedError