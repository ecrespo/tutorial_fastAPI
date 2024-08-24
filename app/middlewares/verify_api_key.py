from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

class APIKeyVerifier:
    """
    APIKeyVerifier class for verifying API keys.

    This class provides methods for verifying API keys. It checks if the provided API key is in the list of valid API keys.
    If the API key is valid, it returns the API key. If the API key is invalid or missing, it raises an HTTPException with a status code of 401 (Unauthorized).

    Attributes:
        api_keys (list[str]): A list of valid API keys.

    Methods:
        __call__(self, api_key_header: str = Security(api_key_header)) -> str: Verifies the API key.
    """

    def __init__(self, api_keys):
        """
        Initializes a new instance of the APIKeyVerifier class.

        Args:
            api_keys (list[str]): The list of valid API keys.
        """
        self.api_keys = api_keys

    def __call__(self, api_key_header: str = Security(api_key_header)) -> str:
        """
        Verifies the API key.

        This method checks if the provided API key is in the list of valid API keys. If the API key is valid, it returns the API key.
        If the API key is invalid or missing, it raises an HTTPException with a status code of 401 (Unauthorized).

        Args:
            api_key_header (str): The API key to verify.

        Returns:
            str: The verified API key.

        Raises:
            HTTPException: If the API key is invalid or missing.
        """
        if api_key_header in self.api_keys:
            return api_key_header
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
