from http import HTTPStatus
from pydantic import EmailStr

from app.core.security import Security
from app.core.util import success_response, error_response
from app.enums.user_type import UserType
from app.models.user import User
from app.services.mongodb_service.mdb_user_service import MDBUserService


class UserService:

    def __init__(self, mdb_user_service: MDBUserService):
        self.mdb_user_service = mdb_user_service

    async def create_user(self, email: EmailStr, password: str, user_type: UserType):
        user = await self.mdb_user_service.get_user_by_email(email=email)
        hashed_password = Security.hash_password(password)

        if user is None:
            user_obj = User(email=email, password=hashed_password)
            await self.mdb_user_service.create_user(user_obj, user_type=user_type)
            return success_response("User created successfully.", HTTPStatus.CREATED)

        return error_response("User already exists.", HTTPStatus.CONFLICT)

    async def authenticate_user(self, email: EmailStr, password: str):
        user = await self.mdb_user_service.get_user_by_email(email=email)
        if not user:
            return error_response("Invalid email or password.", HTTPStatus.UNAUTHORIZED)
        if not Security.verify_password(password, user['password']):
            return  error_response("Invalid email or password.", HTTPStatus.UNAUTHORIZED)

        token = Security.create_access_token(user["email"], user["is_admin"])
        return success_response("User authenticated successfully.", HTTPStatus.OK, data={"token": token})
