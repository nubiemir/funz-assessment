from datetime import datetime, timezone

from pydantic import BaseModel, HttpUrl
import uuid

class Game(BaseModel):
    """
    Pydantic model representing a Game entity.
    """
    id: str
    name: str
    type: str
    publisher_name: str
    external_game_id: str
    description: str | None = None
    is_featured: bool = False
    cover_image_url: HttpUrl
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    likes: list[str] = []
    trailer: HttpUrl | None = None
    collage: list[HttpUrl] = []

    @classmethod
    def create(cls, **data):
        """
        Factory method to create a new Game instance with a UUID and timestamps.
        
        Args:
            **data: Field values for the game
            
        Returns:
            Game: The initialized Game instance
        """
        return cls(
            id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            **data
        )