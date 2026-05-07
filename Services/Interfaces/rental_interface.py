from typing import Tuple


class RentalInterface:
    def create_rental(self, user_id: int, bike_id: int) -> Tuple[bool, str]:
        """
        Rent a bike.
        Returns (success, message).
        """
        raise NotImplementedError

    def return_bike(self, rental_id: int) -> Tuple[bool, str]:
        """
        Return a rented bike.
        Returns (success, message).
        """
        raise NotImplementedError               