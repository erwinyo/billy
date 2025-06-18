import os
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

from api.basemodel.user import UserBaseModel, LoginRequest, SignupRequest
from api.basemodel.token import Token

SECRET_KEY = "secret"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/token")
router = APIRouter(prefix="/api/v1/account", tags=["user"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        user.username, user.id, expires_delta=timedelta(days=365)
    )
    return {"access_token": token, "token_type": "bearer"}


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    if username == os.getenv("API_AUTH_USERNAME") and password == os.getenv(
        "API_AUTH_PASSWORD"
    ):
        return UserBaseModel(
            id=1, username=username, hashed_password=bcrypt_context.hash(password)
        )
    return False


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
