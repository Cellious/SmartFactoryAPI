from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str
