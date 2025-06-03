from pydantic import BaseModel


class UserBaseModel(BaseModel):
    id: int
    username: str
    hashed_password: str


class SignupRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str
