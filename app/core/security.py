from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from pydantic import EmailStr

from app.core.config import settings

class Security:
    """
    Handles security operations including password hashing and JWT management.
    """
    _pwd_context: CryptContext = CryptContext(
        schemes=["pbkdf2_sha256", "bcrypt"], default="pbkdf2_sha256",
                           pbkdf2_sha256__default_rounds=30000)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hashes a plain password using configured schemes.
        
        Args:
            password: The plain text password
            
        Returns:
            str: The hashed password string
        """
        return cls._pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed: str) -> bool:
        """
        Verifies a password against a hash.
        
        Args:
            password: The plain text password
            hashed: The hashed password to verify against
            
        Returns:
            bool: True if password matches hash, False otherwise
        """
        return cls._pwd_context.verify(password, hashed)

    @classmethod
    def create_access_token(cls, subject: EmailStr, is_admin: bool, expires_hours: int = 1) -> str:
        """
        Creates a JWT access token.
        
        Args:
            subject: The subject (email) for the token
            is_admin: Whether the user has admin privileges
            expires_hours: Token validity duration in hours
            
        Returns:
            str: Encoded JWT token string
        """
        payload = {
            "sub": subject,
            "is_admin": is_admin,
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_hours),
            "iss": settings.jwt_app_id
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @classmethod
    def verify_token(cls, token: str) -> dict | None:
        """
        Verifies and decodes a JWT token.
        
        Args:
            token: The JWT token string
            
        Returns:
            dict | None: The decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            return payload
        except jwt.PyJWTError:
            return None