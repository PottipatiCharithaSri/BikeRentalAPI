from typing import Tuple, Dict, List


class RentalInterface:
    
    def get_all_rentals(self) -> List[Dict]:
        raise NotImplementedError

    def get_rental_by_id(self, rental_id: int) -> Dict:
        raise NotImplementedError

    def get_rentals_by_user(self, user_id: int) -> List[Dict]:
        raise NotImplementedError

    def reserve_rental(
        self,
        user_id: int,
        bike_id: int,
        duration_value: int,
        duration_unit: str
    ) -> Tuple[bool, str]:
        raise NotImplementedError

    def start_rental(self, rental_id: int) -> Tuple[bool, str]:
        raise NotImplementedError

    def return_bike(
        self,
        rental_id: int,
        return_reason: str
    ) -> Tuple[bool, str]:
        raise NotImplementedError

    def cancel_rental(
        self,
        rental_id: int,
        cancellation_reason: str
    ) -> Tuple[bool, str]:
        raise NotImplementedError

    def mark_overdue_rentals(self) -> int:
        raise NotImplementedError
