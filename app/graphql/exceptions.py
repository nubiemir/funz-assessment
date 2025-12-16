import strawberry
from strawberry.exceptions import StrawberryException


class GameNotFoundError(StrawberryException):
    def exception_source(self):
        pass

    def __init__(self, game_id: str):
        self.message = f"Game with id {game_id} not found"


class UnauthorizedError(StrawberryException):
    def exception_source(self):
        pass

    def __init__(self, message="Unauthorized"):
        self.message = message


