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
from base.config import logger
from base.exception import BillyResponse
from api.basemodel.utility import EmailRequest
from utils.messaging import send_email


router = APIRouter(prefix="/api/v1/utility", tags=["utility"])


@router.post("/email/send")
def utility_send_email(email: EmailRequest):
    response = send_email(
        subject=email.subject, body=email.body, recipient=email.recipient
    )
    if response is BillyResponse.SERVER_ERROR:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Failed to send email.",
            },
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Success to send email.",
        },
    )
