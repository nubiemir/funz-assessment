import strawberry
from strawberry import Info
from app.core.logger import logger
from app.core.util import ErrorResponse, SuccessResponse
from app.graphql.context import GraphQLContext
from app.graphql.type import GameType
from app.graphql.exceptions import UnauthorizedError, GameNotFoundError


@strawberry.type
class Query:
    """
    Root query type, containing all data retrieval operations.
    """

    @strawberry.field
    async def game(self, game_id: str, info: Info) -> SuccessResponse | ErrorResponse:
        """
        Retrieves a single game by ID.
        
        Args:
            game_id: The ID of the game to retrieve
            info: GraphQL execution info
            
        Returns:
            SuccessResponse | ErrorResponse: The game data or error details
        """
        ctx: GraphQLContext = info.context
        try:
            if not ctx.is_authenticated:
                raise UnauthorizedError("Unauthorized access attempt to view game")

            game = await ctx.gql_game_service.get_game_by_id(game_id)
            if not game:
                raise GameNotFoundError(game_id)

            return SuccessResponse(data=[GameType(**game.model_dump())])

        except (UnauthorizedError, GameNotFoundError) as e:
            logger.warning(f"Error fetching game {game_id}: {e}")
            return ErrorResponse(success=False, message=str(e), code=401)
        except Exception as e:
            logger.error(f"Unexpected error fetching game {game_id}: {e}", exc_info=True)
            return ErrorResponse()

    @strawberry.field
    async def games(self, info: Info) -> SuccessResponse | ErrorResponse:
        """
        Retrieves a list of all games.
        
        Args:
            info: GraphQL execution info
            
        Returns:
            SuccessResponse | ErrorResponse: List of games or error details
        """
        ctx: GraphQLContext = info.context
        try:
            if not ctx.is_authenticated:
                raise UnauthorizedError("Unauthorized access attempt to view games")

            games = await ctx.gql_game_service.list_games()
            return SuccessResponse(data=[GameType(**game.model_dump()) for game in games])

        except UnauthorizedError as e:
            logger.warning(f"Unauthorized access attempt to list games: {e}")
            return ErrorResponse(success=False, message=str(e), code=401)
        except Exception as e:
            logger.error(f"Unexpected error fetching games list: {e}", exc_info=True)
            return ErrorResponse()
