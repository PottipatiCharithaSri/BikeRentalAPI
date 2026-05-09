from typing import Dict, Optional

from Models.user import User

class AuthInterface:
    def login(self, data: Dict) -> Optional[str]:
        """
        Authenticate user and return JWT token.
        Returns token if success, None if failure.
        """
        raise NotImplementedError

    def register(self, data: Dict) -> Optional[User]:
        """
        Register a new user.
        Returns User if success, False if username exists.
        """
        raise NotImplementedError