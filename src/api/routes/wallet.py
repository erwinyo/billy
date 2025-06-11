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
from api.routes.user import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
router = APIRouter(prefix="/v1/wallet", tags=["wallet"])


@router.get("/get")
def get(user: user_dependency, wallet: str):
    billy_web._check_authorized_user(user)

    response = billy_web._get_wallet_data(wallet=wallet)
    if response is BillyResponse.NOT_FOUND:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{wallet}' not found.",
        )
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"{wallet} wallet data retrieved successfully.",
            "data": response,
        },
    )


@router.get("/get_raw")
def get(user: user_dependency, wallet: str):
    billy_web._check_authorized_user(user)

    response = billy_web._get_wallet_raw_data(wallet=wallet)
    if response is BillyResponse.NOT_FOUND:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet}' not found.",
        )
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f" {wallet} wallet data retrieved successfully.",
            "data": response,
        },
    )
