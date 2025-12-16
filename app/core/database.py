from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class MongoDB:
    """
    Singleton manager for MongoDB connection.
    """
    _client: AsyncIOMotorClient | None = None

    @classmethod
    async def connect(cls):
        """
        Initializes the MongoDB connection pool.
        Should be called on app startup.
        """
        if cls._client is None:
            cls._client = AsyncIOMotorClient(settings.mongo_uri)
        return cls._client

    @classmethod
    async def close(cls):
        """
        Closes the MongoDB connection pool.
        Should be called on app shutdown.
        """
        if cls._client is not None:
            cls._client.close()
            cls._client = None

    @classmethod
    def get_db(cls):
        """
        Retrieves the database instance.
        
        Returns:
            Database: The AsyncIOMotorDatabase instance
            
        Raises:
            RuntimeError: If client is not initialized
        """
        if cls._client is None:
            raise RuntimeError("Mongo client is not initialized")
        return cls._client[settings.mongo_db] # type: ignore
