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


import os
import requests


def _make_a_request_to_api(
    route: str,
    method: str = "GET",
    data: dict = None,
    params: dict = None,
    headers: dict = {},
    type_of_request: str = "json",
) -> tuple[int, dict]:
    url = f"http://{os.getenv('HOST')}:{os.getenv('PORT')}{route}"

    method = method.upper()
    assert method in ["GET", "POST"], "Method must be GET or POST"

    # Set appropriate Content-Type header
    if type_of_request == "json":
        headers = {"Content-Type": "application/json", **headers}
    elif type_of_request == "form":
        headers = {"Content-Type": "application/x-www-form-urlencoded", **headers}
        if data is not None:
            data = {str(k): str(v) for k, v in data.items()}

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            if type_of_request == "json":
                response = requests.post(url, headers=headers, json=data)
            elif type_of_request == "form":
                response = requests.post(url, headers=headers, data=data)

        return response.status_code, response.json()

    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to make request to {url} with method {method}: {str(e)}"
        ) from e
    except ValueError as e:
        raise RuntimeError(f"Failed to parse JSON response from {url}: {str(e)}") from e
