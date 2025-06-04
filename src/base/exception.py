# Builtin imports
import os
import sys
from enum import Enum
from datetime import datetime

# Third-party imports

# Local imports


class BillyResponseError(Enum):
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "Unauthorized access"
    INVALID_INPUT = "Invalid input"
    SERVER_ERROR = "Internal server error"
    FORBIDDEN = "Forbidden"
