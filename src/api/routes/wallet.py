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
from utils.database import _get_table_data
from api.routes.user import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
router = APIRouter(prefix="/v1/wallet", tags=["wallet"])


def __check_authorized_user(user: user_dependency) -> None:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )


def __get_account_wallets(account_id: str) -> list:
    # Retrieve data from 'account' table
    account_data = _get_table_data(
        table_name="account",
        condition={"account_id": account_id},
    )

    # Extract wallets from the account data
    wallets = account_data[0].get("wallets", [])
    return wallets


def __get_pay_ids_from_account_id(account_id: str) -> list:
    # Retrieve data from 'account_pay' table
    account_pay_ids = _get_table_data(
        table_name="account_pay",
        condition={"account_id": account_id},
    )
    pay_ids = [account_pay_id["pay_id"] for account_pay_id in account_pay_ids]
    return pay_ids


def __get_wallet_raw_data(account_id: str, wallet: str) -> dict:
    # Normalize wallet name to lowercase (ensure non-sensitive case)
    wallet = wallet.lower()
    # Check if the account has the specified wallet
    wallets = __get_account_wallets(account_id=account_id)
    if wallet not in wallets:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{wallet}' not found for account ID '{account_id}'.",
        )

    pay_ids = __get_pay_ids_from_account_id(account_id=account_id)
    # Retrieve data from 'pay' table
    datas = _get_table_data(
        table_name="pay",
        condition={"pay_id": pay_ids, "wallet": wallet, "active": True},
    )
    return datas


@router.get("/get")
def get_freedom_fund(user: user_dependency, account_id: str, wallet: str):
    __check_authorized_user(user)

    response = __get_wallet_raw_data(account_id=account_id, wallet=wallet)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f" {wallet} wallet data retrieved successfully.",
            "data": response,
        },
    )
