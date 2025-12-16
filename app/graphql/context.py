from strawberry.fastapi import BaseContext
from fastapi import Request
from app.services.graphql_service.gql_game_service import GqlGameService
from app.core.security import Security

class GraphQLContext(BaseContext):
    """
    Context for GraphQL operations, holding request, user, and service instances.
    """
    def __init__(self, request: Request):
        super().__init__()
        self.request = request
        self.gql_game_service = GqlGameService()
        self.user = self.get_current_user()

    def get_current_user(self):
        """
        Extracts and verifies the current user from the Authorization header.
        
        Returns:
            dict | None: The user payload if authenticated, None otherwise
        """
        authorization = self.request.headers.get("Authorization")
        if not authorization:
            return None
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return None
            
            payload = Security.verify_token(token)
            return payload
        except (ValueError, Exception):
            return None

    @property
    def is_authenticated(self) -> bool:
        """Checks if the context has an authenticated user."""
        return self.user is not None

    @property
    def is_admin(self) -> bool:
        """Checks if the authenticated user has admin privileges."""
        return self.user and self.user.get("is_admin", False)