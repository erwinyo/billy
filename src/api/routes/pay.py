# Built-in imports
import os
import io
import sys
import uuid
import random
import json
import time
import base64
from typing import Annotated, Union

# Third-party imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile
from fastapi.responses import Response, JSONResponse, FileResponse, StreamingResponse


# Local imports
from base.config import logger
from utils.database import _get_table_data, _insert_to_postgres
from utils.utils import _generate_unique_id, _generate_timestamp
from api.routes.user import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
router = APIRouter(prefix="/v1/pay", tags=["pay"])


def __check_authorized_user(user: user_dependency) -> None:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )


def __insert_pay_data(
    account_id: str, wallet: str, flow: str, description: str, issued: float
) -> None:
    # Insert 'pay' table
    pay_id = _generate_unique_id()
    _insert_to_postgres(
        table_name="pay",
        data={
            "pay_id": pay_id,
            "wallet": wallet,
            "flow": flow,
            "created_at": _generate_timestamp(),
            "description": description,
            "issued": issued,
            "active": True,
        },
    )

    # Insert 'account_pay' table
    _insert_to_postgres(
        table_name="account_pay",
        data={
            "account_id": account_id,
            "pay_id": pay_id,
        },
    )


@router.post("/in")
def pay_in(
    user: user_dependency,
    account_id: str,
    wallet: str,
    description: str,
    issued: float,
):
    __check_authorized_user(user)
    __insert_pay_data(
        account_id=account_id,
        wallet=wallet,
        flow="IN",
        description=description,
        issued=issued,
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
    account_id: str,
    wallet: str,
    description: str,
    issued: float,
):
    __check_authorized_user(user)
    __insert_pay_data(
        account_id=account_id,
        wallet=wallet,
        flow="OUT",
        description=description,
        issued=issued,
    )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Pay OUT data inserted successfully.",
        },
    )
