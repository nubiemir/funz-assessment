from fastapi import APIRouter, Depends
from app.enums.user_type import UserType
from app.models.user import User
from app.services.mongodb_service.mdb_user_service import MDBUserService
from app.services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service() -> UserService:
    """
    Dependency to provide a UserService instance.
    
    Returns:
        UserService: Initialized service with MongoDB backend
    """
    mdb_user_service = MDBUserService()
    return UserService(mdb_user_service)


@router.post("/signup/{user_type}")
async def signup(user_type: UserType, user: User, user_service: UserService = Depends(get_user_service)):
    """
    Registers a new user.
    
    Args:
        user_type: The type of user (e.g., ADMIN, USER)
        user: The user registration data
        user_service: Service for user operations
        
    Returns:
        dict: The result of the creation operation
    """
    return await user_service.create_user(user.email, user.password, user_type)


@router.post("/login")
async def login(user: User, user_service: UserService = Depends(get_user_service)):
    """
    Authenticates a user and returns a token.
    
    Args:
        user: The login credentials
        user_service: Service for user operations
        
    Returns:
        dict: Authentication result containing the token
    """
    return await user_service.authenticate_user(user.email, user.password)

