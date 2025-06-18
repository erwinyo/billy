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
from utils.messaging import send_email

router = APIRouter(prefix="/api/v1/utility", tags=["utility"])


@router.post("/email/send")
def utility_send_email(subject: str, body: str, recipient: str):
    success = send_email(subject=subject, body=body, recipient=recipient)
    if not success:
        return BillyResponse.SERVER_ERROR
    return BillyResponse.SUCCESS
