# Builtin imports
import os
import sys
from enum import Enum
from datetime import datetime

# Third-party imports

# Local imports


class BillyResponse(Enum):
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "Unauthorized access"
    BAD_REQUEST = "Bad request"
    INVALID_INPUT = "Invalid input"
    SERVER_ERROR = "Internal server error"
    FORBIDDEN = "Forbidden"
    SUCCESS = "Operation completed successfully"
