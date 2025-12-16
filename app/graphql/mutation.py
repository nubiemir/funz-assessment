import strawberry
from strawberry import Info

from app.core.util import ErrorResponse, SuccessResponse
from app.graphql.context import GraphQLContext
from app.graphql.exceptions import GameNotFoundError, UnauthorizedError
from app.graphql.type import GameType, GameInput
from app.models.game import Game
from app.core.logger import logger


@strawberry.type
class Mutation:
    """
    Root mutation type, containing all data modification operations.
    """

    @strawberry.mutation
    async def create_game(self, game_input: GameInput, info: Info) -> SuccessResponse | ErrorResponse:
        """
        Creates a new game.
        
        Args:
            game_input: The input data for the new game
            info: GraphQL execution info
            
        Returns:
            SuccessResponse | ErrorResponse: The created game or error details
        """
        ctx: GraphQLContext = info.context
        try:
            if not ctx.is_admin:
                raise UnauthorizedError("Unauthorized attempt to create game")

            game = Game.create(**game_input.__dict__)
            created_game = await ctx.gql_game_service.create_game(game)
            return SuccessResponse(data=[GameType(**created_game.model_dump())])

        except UnauthorizedError as e:
            logger.warning(f"Unauthorized attempt to create game: {e}")
            return ErrorResponse(success=False, message=str(e), code=401)
        except Exception as e:
            logger.error(f"Unexpected error during game creation: {e}", exc_info=True)
            return ErrorResponse()

    @strawberry.mutation
    async def update_game(self, game_id: str, game_input: GameInput, info: Info) -> SuccessResponse | ErrorResponse:
        """
        Updates an existing game.
        
        Args:
            game_id: The ID of the game to update
            game_input: The new data for the game
            info: GraphQL execution info
            
        Returns:
            SuccessResponse | ErrorResponse: The updated game or error details
        """
        ctx: GraphQLContext = info.context
        try:
            if not ctx.is_admin:
                raise UnauthorizedError("Unauthorized attempt to update game")

            game = await ctx.gql_game_service.get_game_by_id(game_id)
            if game is None:
                raise GameNotFoundError(game_id)

            updated_game = await ctx.gql_game_service.update_game(game_id, game_input.__dict__)
            return SuccessResponse(data=[GameType(**updated_game.model_dump())])

        except (UnauthorizedError, GameNotFoundError) as e:
            logger.warning(f"Error updating game {game_id}: {e}")
            return ErrorResponse(success=False, message=str(e), code=401)
        except Exception as e:
            logger.error(f"Unexpected error during game update {game_id}: {e}", exc_info=True)
            return ErrorResponse()

    @strawberry.mutation
    async def delete_game(self, game_id: str, info: Info) -> SuccessResponse | ErrorResponse:
        """
        Deletes a game.
        
        Args:
            game_id: The ID of the game to delete
            info: GraphQL execution info
            
        Returns:
            SuccessResponse | ErrorResponse: The deleted game data or error details
        """
        ctx: GraphQLContext = info.context
        try:
            if not ctx.is_admin:
                raise UnauthorizedError("Unauthorized attempt to delete game")

            game = await ctx.gql_game_service.get_game_by_id(game_id)
            if game is None:
                raise GameNotFoundError(game_id)

            await ctx.gql_game_service.delete_game(game_id)
            return SuccessResponse(data=[GameType(**game.model_dump())])

        except (UnauthorizedError, GameNotFoundError) as e:
            logger.warning(f"Error deleting game {game_id}: {e}")
            return ErrorResponse(success=False, message=str(e), code=401)
        except Exception as e:
            logger.error(f"Unexpected error during game deletion {game_id}: {e}", exc_info=True)
            return ErrorResponse()

    @strawberry.mutation
    async def toggle_like_game(self, game_id: str, user_id: str, info: Info) -> SuccessResponse | ErrorResponse:
        """
        Toggles the 'like' status of a game for a user.
        
        Args:
            game_id: The ID of the game
            user_id: The ID of the user liking the game
            info: GraphQL execution info
            
        Returns:
            SuccessResponse | ErrorResponse: The updated game state or error details
        """
        ctx: GraphQLContext = info.context
        try:
            if not ctx.is_authenticated:
                raise UnauthorizedError("Unauthorized attempt to toggle like game")

            game = await ctx.gql_game_service.get_game_by_id(game_id)
            if game is None:
                raise GameNotFoundError(game_id)

            user_str = str(user_id)
            likes: list[str] = game.__dict__.get("likes", [])
            if user_str in likes:
                likes.remove(user_str)
            else:
                likes.append(user_str)

            toggled_game = await ctx.gql_game_service.toggle_like_game(game_id, likes)
            return SuccessResponse(data=[GameType(**toggled_game.model_dump())])

        except (UnauthorizedError, GameNotFoundError) as e:
            logger.warning(f"Error toggling like for game {game_id} by user {user_id}: {e}")
            return ErrorResponse(success=False, message=str(e), code=401)
        except Exception as e:
            logger.error(f"Unexpected error toggling like for game {game_id} by user {user_id}: {e}", exc_info=True)
            return ErrorResponse()
