# Built-in package
import os
from enum import Enum
from datetime import datetime
from typing import Annotated, Union
from dataclasses import dataclass, field

# Third party package
import psycopg2
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile
from fastapi.responses import Response, JSONResponse, FileResponse, StreamingResponse


# Local package
from base.config import logger
from base.exception import BillyResponse
from utils.database import (
    _get_table_data,
    _insert_to_postgres,
    _set_client_database,
    _check_postgres_connection,
)
from utils.utils import (
    _generate_unique_id,
    _generate_timestamp_now,
    _make_a_request_to_api,
)

load_dotenv()


@dataclass(frozen=False, kw_only=False, match_args=False, slots=False)
class BillyWeb:
    config: dict = field(default_factory=dict)

    _account_id: str = field(init=False, repr=False)
    _postgres_connection: str = field(init=False, repr=False)
    _post: str = field(init=False, repr=False)
    _account_id: str = field(init=False, repr=False)
    _account_id: str = field(init=False, repr=False)
    _account_id: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # Create database connection
        self._postgres_connection = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )
        self._postgres_cursor = self._postgres_connection.cursor()
        _set_client_database(
            postgres_connection=self._postgres_connection,
            postgres_cursor=self._postgres_cursor,
        )

        # Account informations
        self._account_id = "7edd7933-b9bb-49b9-ad86-e12bbf380994"
        self._beared_token = None
        self._default_wallets = [
            "freedom_fund",
            "savings",
            "business",
            "charity",
            "daily_needs",
        ]

    def __get_beared_token(self, username: str, password: str) -> str:
        print(f"Username: {username}, Password: {password} --------- asdasd")
        status_code, response = _make_a_request_to_api(
            route="/user/token",
            method="POST",
            data={"username": username, "password": password},
        )
        print(f"Status code: {status_code}, Response: {response}")
        if status_code != 200:
            logger.error(
                f"Failed to login with status code {status_code} and response: {response}"
            )
            return None

        beared_token = response.get("access_token")
        return beared_token

    def _login_authorized_user(self, username: str, password: str) -> BillyResponse:
        if self._beared_token is not None:
            return BillyResponse.BAD_REQUEST

        # Login
        print(f"Username: {username}, Password: {password} --------- ")
        beared_token = self.__get_beared_token(username=username, password=password)
        if beared_token == "string":
            logger.error("Invalid username or password.")
            return None
        if beared_token is None:
            return BillyResponse.INVALID_INPUT

        self._user_name = username
        self._user_passowrd = password
        logger.info(f"Authorized user logged in: {self._user_name}")

        return BillyResponse.SUCCESS

    def _check_authorized_user(self, user: Annotated) -> None:
        if user is None:
            JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "message": "Unauthorized user.",
                },
            )

    def _register_account(
        self,
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
                "wallets": self._default_wallets,
                "created_at": _generate_timestamp_now(),
            },
        )

    def _insert_pay_data(
        self,
        wallet: str,
        flow: str,
        description: str,
        issued: float,
        created_at: datetime,
    ) -> None:
        # Insert 'pay' table
        pay_id = _generate_unique_id()
        _insert_to_postgres(
            table_name="pay",
            data={
                "pay_id": pay_id,
                "wallet": wallet,
                "flow": flow,
                "created_at": created_at,
                "description": description,
                "issued": issued,
                "active": True,
            },
        )

        # Insert 'account_pay' table
        _insert_to_postgres(
            table_name="account_pay",
            data={
                "account_id": self._account_id,
                "pay_id": pay_id,
            },
        )

    def __get_account_wallets(self, account_id: str) -> list:
        # Retrieve data from 'account' table
        account_data = _get_table_data(
            table_name="account",
            condition={"account_id": self._account_id},
        )

        # Extract wallets from the account data
        wallets = account_data[0].get("wallets", [])
        logger.debug(f"Retrieved wallets for account {account_id}: {wallets}")
        return wallets

    def __get_pay_ids_from_account_id(self) -> list:
        # Retrieve data from 'account_pay' table
        account_pay_ids = _get_table_data(
            table_name="account_pay",
            condition={"account_id": self._account_id},
        )
        pay_ids = [account_pay_id["pay_id"] for account_pay_id in account_pay_ids]
        logger.debug(f"Retrieved pay IDs for account {self._account_id}: {pay_ids}")
        return pay_ids

    def _get_wallet_raw_data(self, wallet: str) -> dict:
        # Normalize wallet name to lowercase (ensure non-sensitive case)
        wallet = wallet.lower()
        # Check if the account has the specified wallet
        wallets = self.__get_account_wallets(account_id=self._account_id)
        if wallet not in wallets:
            return BillyResponse.NOT_FOUND

        pay_ids = self.__get_pay_ids_from_account_id()
        # Check if there no pay IDs associated with the account
        if not pay_ids:
            return []

        # Retrieve data from 'pay' table
        datas = _get_table_data(
            table_name="pay",
            condition={"pay_id": pay_ids, "wallet": wallet, "active": True},
            order_by="created_at",
        )
        return datas

    def _get_wallet_data(self, wallet: str) -> dict:
        raw_datas = self._get_wallet_raw_data(wallet=wallet)
        if raw_datas is BillyResponse.NOT_FOUND:
            return BillyResponse.NOT_FOUND

        results = {}
        for data in raw_datas:
            pay_id = data["pay_id"]
            wallet = data["wallet"]
            flow = data["flow"]
            created_at = datetime.fromisoformat(data["created_at"])
            description = data["description"]
            issued = data["issued"]
            active = data["active"]

            # Initialize the results structure if not already present
            if created_at.year not in results:
                results[created_at.year] = {}
            if created_at.month not in results[created_at.year]:
                results[created_at.year][created_at.month] = {
                    "BUDGET": 0,
                    "IN": {"data": [], "total": 0},
                    "OUT": {"data": [], "total": 0},
                    "READY_TO_SPEND": 0,
                }

            # Create a data entry for the current pay record
            if flow == "IN":
                results[created_at.year][created_at.month]["IN"]["data"].append(data)
                results[created_at.year][created_at.month]["IN"]["total"] += issued
            elif flow == "OUT":
                results[created_at.year][created_at.month]["OUT"]["data"].append(data)
                results[created_at.year][created_at.month]["OUT"]["total"] += issued

        # Setting up BUDGET and READY_TO_SPEND
        # Sort years and months for correct chronological order
        prev_budget = 0
        for year in results.keys():
            for month in results[year]:
                data = results[year][month]

                data["BUDGET"] = prev_budget
                # Calculate READY_TO_SPEND as BUDGET + IN - OUT
                data["READY_TO_SPEND"] = (
                    data["BUDGET"] + data["IN"]["total"] - data["OUT"]["total"]
                )
                prev_budget = data["READY_TO_SPEND"]

        return results
