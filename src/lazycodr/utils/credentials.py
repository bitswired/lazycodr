import json
from functools import wraps
from pathlib import Path


class CredentialsNotFoundError(Exception):
    """Exception raised when the credentials file is not found."""

    def __init__(self, path):
        self.path = path
        self.message = f"Credentials file not found at {path}"
        super().__init__(self.message)


def check_credentials():
    """Check if credentials file exists."""
    credentials_path = Path.home() / ".lazy-coder-credentials.json"
    try:
        with Path.open(credentials_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError as err:
        raise CredentialsNotFoundError(credentials_path) from err


# Decorator that loads and provides credentials to the function
# use funcools.wraps to preserve the function name and docstring
def use_credentials(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        credentials = check_credentials()
        return func(credentials, *args, **kwargs)

    return wrapper
