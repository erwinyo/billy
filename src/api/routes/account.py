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
from base.config import logger, billy_web
from base.exception import BillyResponse
from utils.database import _get_table_data, _insert_to_postgres
from utils.utils import _generate_unique_id, _generate_timestamp_now
from api.routes.user import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
router = APIRouter(prefix="/v1/account", tags=["account"])


@router.post("/signup")
def signup(
    user: user_dependency,
    full_name: str,
    email: str,
    telp: str,
    password: str,
    pin: str,
):
    billy_web._check_authorized_user(user)
    billy_web._register_account(
        full_name=full_name, email=email, telp=telp, password=password, pin=pin
    )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Account registered successfully.",
        },
    )


@router.post("/login")
def login(username: str, password: str):
    print(username, password)
    response = billy_web._login_authorized_user(username=username, password=password)
    if response is BillyResponse.INVALID_INPUT:
        raise HTTPException(
            status_code=401,
            detail="Username or password is incorrect.",
        )
    elif response is BillyResponse.BAD_REQUEST:
        raise HTTPException(
            status_code=404,
            detail="Already logged in, please logout first.",
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": response,
        },
    )
