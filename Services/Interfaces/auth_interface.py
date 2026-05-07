from typing import Dict, Optional

class AuthInterface:
    def login(self, data: Dict) -> Optional[str]:
        """
        Authenticate user and return JWT token.
        Returns token if success, None if failure.
        """
        raise NotImplementedError

    def register(self, data: Dict) -> bool:
        """
        Register a new user.
        Returns True if success, False if username exists.
        """
        raise NotImplementedError