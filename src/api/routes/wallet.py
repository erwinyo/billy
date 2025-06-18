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

router = APIRouter(prefix="/api/v1/wallet", tags=["wallet"])


@router.get("/get_pay")
def get_pay(account_id: str, wallet: str):
    response = billy_web._get_wallet_pay_data(account_id=account_id, wallet=wallet)
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


@router.get("/get_pay_raw")
def get(account_id: str, wallet: str):
    response = billy_web._get_wallet_pay_raw_data(account_id=account_id, wallet=wallet)
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


@router.get("/get_wallets")
def get(account_id: str):
    response = billy_web._get_wallets(account_id=account_id)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"wallet data retrieved successfully.",
            "data": response,
        },
    )
