import uuid

from pydantic import EmailStr

from app.core.database import MongoDB
from app.enums.user_type import UserType
from app.models.user import UserInDB, User


class MDBUserService:
    def __init__(self):
        self.mongo_cls = MongoDB.get_db()

    async def get_user_by_email(self, email: EmailStr) -> UserInDB:
        user = await self.mongo_cls.users.find_one({"email": email})
        if user:
            user["id"] = str(user["_id"])
            user.pop("_id", None)
        return user

    async def create_user(self, user: User, user_type: UserType) -> UserInDB:
        user = {
            "_id": str(uuid.uuid4()),
            "email": user.email,
            "password": user.password,
            "is_admin": True if user_type is UserType.admin else False,
        }

        return  await self.mongo_cls.users.insert_one(user)