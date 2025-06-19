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
from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile
from fastapi.responses import Response, JSONResponse, FileResponse, StreamingResponse

# Local imports
from base.config import logger, billy_web
from base.exception import BillyResponse

router = APIRouter(prefix="/api/v1/account", tags=["account"])


@router.post("/signup")
def signup(
    full_name: str,
    email: str,
    telp: str,
    password: str,
    pin: str,
):
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
            "message": "Logged in successfully.",
        },
    )


@router.get("/telegram/login")
def telegram_login(email: str, telegram_id: str):
    """
    USED IN EMAIL LINK LOGIN
    """
    response = billy_web._validate_email_link(email=email, telegram_id=telegram_id)

    if response is BillyResponse.NOT_FOUND:
        raise HTTPException(
            status_code=404,
            detail="Email not found you can register first.",
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Login email successfully sent.",
        },
    )


@router.post("/telegram/session")
def telegram_session(telegram_id: str):
    response, account_id = billy_web._validate_telegram_session(telegram_id=telegram_id)
    if response is BillyResponse.UNAUTHORIZED:
        raise HTTPException(
            status_code=401,
            detail="Telegram session is not valid or expired.",
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Session authorized.",
            "data": account_id,
        },
    )
