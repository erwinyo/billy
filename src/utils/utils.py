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


def _generate_timestamp_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def _generate_timestamp_custom(
    year: int,
    month: int,
    day: int,
    hour: int = None,
    minute: int = None,
    second: int = None,
):
    if hour is None:
        hour = random.randint(1, 23)
    if minute is None:
        minute = random.randint(1, 59)
    if second is None:
        second = random.randint(1, 59)
    dt = datetime(year, month, day, hour, minute, second).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )
    return dt
