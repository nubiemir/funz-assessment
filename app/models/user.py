import uuid

from pydantic import BaseModel, EmailStr

class UserInDB(BaseModel):
    id: str
    email: EmailStr
    password: str
    is_admin: bool


class User(BaseModel):
    email: EmailStr
    password: str