import strawberry
from fastapi.responses import JSONResponse
from app.graphql.type import GameType


def success_response(message: str, status_code: int = 400, data: dict = None) -> JSONResponse:
    """
    Constructs a uniform JSON success response.
    
    Args:
        message: Success message
        status_code: HTTP status code
        data: Optional data payload
        
    Returns:
        JSONResponse: Formatted JSON response
    """
    return JSONResponse(
        status_code=status_code,
        content={"success": True, "message": message, "data": data}
    )


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """
    Constructs a uniform JSON error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        
    Returns:
        JSONResponse: Formatted JSON response
    """
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message}
    )


@strawberry.type
class SuccessResponse:
    success: bool = True
    message: str = "Success"
    code: int = 200
    data: list[GameType]  | None = None

@strawberry.type
class ErrorResponse:
    message: str = "An error occurred"
    data: list[GameType] | None = None
    success: bool = False
    code: int = 500