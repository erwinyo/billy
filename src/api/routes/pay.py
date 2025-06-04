# Built-in imports
import os
import io
import sys
import uuid
import random
import json
import time
import base64
from enum import Enum
from datetime import datetime
from typing import Annotated, Union

# Third-party imports
import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile
from fastapi.responses import Response, JSONResponse, FileResponse, StreamingResponse


# Local imports
from base.config import logger, billy_web
from api.routes.user import get_current_user
from utils.database import _get_table_data, _insert_to_postgres
from utils.utils import _generate_unique_id, _generate_timestamp_now


user_dependency = Annotated[dict, Depends(get_current_user)]
router = APIRouter(prefix="/v1/pay", tags=["pay"])


class FlowType(Enum):
    IN = "IN"
    OUT = "OUT"


@router.post("/in")
def pay_in(
    user: user_dependency,
    wallet: str,
    description: str,
    issued: float,
    created_at: datetime,
):
    billy_web._check_authorized_user(user)
    billy_web._insert_pay_data(
        wallet=wallet,
        flow=FlowType.IN,
        description=description,
        issued=issued,
        created_at=created_at,
    )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Pay IN data inserted successfully.",
        },
    )


@router.post("/out")
def pay_out(
    user: user_dependency,
    wallet: str,
    description: str,
    issued: float,
    created_at: datetime,
):
    billy_web._check_authorized_user(user)
    billy_web._insert_pay_data(
        wallet=wallet,
        flow=FlowType.OUT,
        description=description,
        issued=issued,
        created_at=created_at,
    )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Pay OUT data inserted successfully.",
        },
    )
