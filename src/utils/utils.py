# Built-in imports
import os
import uuid
import random
import string
import urllib.parse
from datetime import datetime

# Third-party imports
import requests
import numpy as np
from PIL import Image
from fastapi.responses import JSONResponse

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


def _make_a_request_to_api(
    route: str,
    method: str = "GET",
    data: dict = None,
    params: dict = None,
    headers: dict = {},
) -> tuple[int, dict]:
    url = f"http://{os.getenv('HOST')}:{os.getenv('PORT')}{route}"
    headers = {"Content-Type": "application/json", **headers}

    if method.upper() == "GET":
        response = requests.get(url, headers=headers, params=params)
    elif method.upper() == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        print(f"Unsupported method: {method}")
        return 400, {"error": "Unsupported method"}

    return response.status_code, response.json()
