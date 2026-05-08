from typing import Tuple, Dict, List

class RentalInterface:
    def get_all_rentals(self) -> List[Dict]:
        raise NotImplementedError

    def get_rental_by_id(self, rental_id: int) -> Dict:
        raise NotImplementedError

    def create_rental(self, user_id: int, bike_id: int) -> Tuple[bool, str]:
        raise NotImplementedError

    def return_bike(self, rental_id: int) -> Tuple[bool, str]:
        raise NotImplementedError

    def cancel_rental(self, rental_id: int) -> Tuple[bool, str]:
        raise NotImplementedError