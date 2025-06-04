# Built-in imports
import os
import sys

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Third-party imports

# Local imports
from base.config import logger, billy_web
from utils.utils import _generate_timestamp_custom

inputs = [
    {
        "wallet": "freedom_fund",
        "flow": "IN",
        "description": "BUDGET(SUNTIK)",
        "issued": 800000,
        "created_at": _generate_timestamp_custom(2025, 4, 1),
    },
    {
        "wallet": "freedom_fund",
        "flow": "IN",
        "description": "BUDGET(ASLI)",
        "issued": 800000,
        "created_at": _generate_timestamp_custom(2025, 4, 9),
    },
    {
        "wallet": "freedom_fund",
        "flow": "IN",
        "description": "BUDGET(SUNTIK)",
        "issued": 516877,
        "created_at": _generate_timestamp_custom(2025, 5, 1),
    },
    {
        "wallet": "freedom_fund",
        "flow": "IN",
        "description": "BUDGET",
        "issued": 800000,
        "created_at": _generate_timestamp_custom(2025, 5, 7),
    },
    {
        "wallet": "freedom_fund",
        "flow": "IN",
        "description": "FADZAR BURGER",
        "issued": 23000,
        "created_at": _generate_timestamp_custom(2025, 5, 16),
    },
    {
        "wallet": "freedom_fund",
        "flow": "IN",
        "description": "SHOPEE",
        "issued": 17457,
        "created_at": _generate_timestamp_custom(2025, 5, 18),
    },
    {
        "wallet": "freedom_fund",
        "flow": "IN",
        "description": "SUNTIK DANA",
        "issued": 400000,
        "created_at": _generate_timestamp_custom(2025, 5, 20),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "FARMERS MARKETS",
        "issued": 21400,
        "created_at": _generate_timestamp_custom(2025, 5, 1),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "AGAM",
        "issued": 33000,
        "created_at": _generate_timestamp_custom(2025, 5, 2),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "TIKET BIOKSKOP PT1",
        "issued": 36900,
        "created_at": _generate_timestamp_custom(2025, 5, 4),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "TIKET + GAP WIDITRA AGAM",
        "issued": 11000,
        "created_at": _generate_timestamp_custom(2025, 5, 4),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "FAMILY MART",
        "issued": 10000,
        "created_at": _generate_timestamp_custom(2025, 5, 4),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "ES KRIM",
        "issued": 8000,
        "created_at": _generate_timestamp_custom(2025, 5, 5),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "COKLAT FARMERS",
        "issued": 25000,
        "created_at": _generate_timestamp_custom(2025, 5, 5),
    },
    {
        "wallet": "freedom_fund",
        "flow": "OUT",
        "description": "PERLENGKAPAN EXHBITION",
        "issued": 68531,
        "created_at": _generate_timestamp_custom(2025, 5, 7),
    },
]


def test_input_data_pay():
    for input in inputs:
        wallet = input["wallet"]
        flow = input["flow"]
        description = input["description"]
        issued = input["issued"]
        created_at = input["created_at"]

        billy_web._insert_pay_data(
            wallet=wallet,
            flow=flow,
            description=description,
            issued=issued,
            created_at=created_at,
        )
