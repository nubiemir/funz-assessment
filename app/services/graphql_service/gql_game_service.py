from datetime import datetime, timezone

from app.core.database import MongoDB
from app.models.game import Game


class GqlGameService:
    """
    Service layer defining business logic for Game operations.
    Interacts with MongoDB.
    """
    def __init__(self):
        self.mongo_cls = MongoDB.get_db()

    async def get_game_by_id(self, game_id: str) -> Game | None:
        """
        Retrieves a game document by its ID.
        
        Args:
            game_id: The unique identifier of the game
            
        Returns:
            Game | None: The game model if found, None otherwise
        """
        game = await self.mongo_cls.games.find_one({"_id": game_id})
        if game is not None:
            game["id"] = game.pop("_id")
            return Game(**game)

        return None


    async def list_games(self) -> list[Game]:
        """
        Retrieves all games from the database.
        
        Returns:
            list[Game]: A list of all game models
        """
        games_list = self.mongo_cls.games.find()
        games = []
        async for doc in games_list:
            doc["id"] = doc.pop("_id")
            games.append(Game(**doc))

        return games


    async def create_game(self, game: Game) -> Game:
        """
        Creates a new game document in the database.
        
        Args:
            game: The game model to persist
            
        Returns:
            Game: The created game model
        """
        doc = game.model_dump()
        doc["_id"] = doc.pop("id")
        doc["cover_image_url"] = str(doc.pop("cover_image_url"))
        await self.mongo_cls.games.insert_one(doc)
        return game

    async def update_game(self, game_id: str, game: Game) -> Game | None:
        """
        Updates an existing game document.
        
        Args:
            game_id: The ID of the game to update
            game: The new game data (partial updates not yet fully supported by this signature)
            
        Returns:
            Game | None: The updated game model if found, None otherwise
        """
        doc = game
        doc["cover_image_url"] = str(doc.pop("cover_image_url"))
        doc["updated_at"] = datetime.now(timezone.utc)
        result = await self.mongo_cls.games.find_one_and_update(
            {"_id": game_id},
            {"$set": doc},
            return_document= True
        )

        if not result:
            return None

        result["id"] = result.pop("_id")
        return Game(**result)

    async def toggle_like_game(self, game_id: str, likes: list[str]) -> Game | None:
        """
        Updates the list of likes for a game.
        
        Args:
            game_id: The ID of the game
            likes: The new list of user IDs who liked the game
            
        Returns:
            Game | None: The updated game model if found, None otherwise
        """
        result = await self.mongo_cls.games.find_one_and_update(
            {"_id": game_id},
            {"$set": {"likes": likes}},
            return_document=True
        )

        if not result:
            return None

        updated_likes = result.get("likes", [])
        result["likes"] = updated_likes
        result["id"] = str(result.pop("_id"))
        return Game(**result)

    async def delete_game(self, game_id: str) -> bool:
        """
        Deletes a game document by ID.
        
        Args:
            game_id: The ID of the game to delete
            
        Returns:
            bool: True if a document was deleted, False otherwise
        """
        result = await self.mongo_cls.games.delete_one({"_id": game_id})
        return result.deleted_count == 1