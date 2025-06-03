# Built-in imports
import os
import uuid
import random
import string
import urllib.parse
from datetime import datetime


# Third-party imports
import numpy as np
from PIL import Image


# Local imports


def _generate_unique_id() -> str:
    return str(uuid.uuid4())


def _generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
