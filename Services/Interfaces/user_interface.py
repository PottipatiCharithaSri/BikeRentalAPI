from typing import List, Dict

class UserInterface:
    def get_all_users(self) -> List[Dict]:
        raise NotImplementedError

    def get_user_by_id(self, user_id: int) -> Dict:
        raise NotImplementedError

    def create_user(self, data: Dict) -> None:
        raise NotImplementedError

    def update_user(self, user_id: int, data: Dict):
        raise NotImplementedError

    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError
