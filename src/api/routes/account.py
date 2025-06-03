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
router = APIRouter(prefix="/v1/account", tags=["account"])

DEFAULT_WALLETS = ["freedom_fund", "savings", "business", "charity", "daily_needs"]


def __check_authorized_user(user: user_dependency) -> None:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )


def __register_account(
    full_name: str,
    email: str,
    telp: str,
    password: str,
    pin: str,
) -> dict:
    _insert_to_postgres(
        table_name="account",
        data={
            "account_id": _generate_unique_id(),
            "full_name": full_name,
            "email": email,
            "telp": telp,
            "password": password,
            "pin": pin,
            "wallets": DEFAULT_WALLETS,
            "created_at": _generate_timestamp(),
        },
    )


@router.post("/signup")
def signup(
    user: user_dependency,
    full_name: str,
    email: str,
    telp: str,
    password: str,
    pin: str,
):
    __check_authorized_user(user)
    __register_account(
        full_name=full_name, email=email, telp=telp, password=password, pin=pin
    )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Account registered successfully.",
        },
    )
