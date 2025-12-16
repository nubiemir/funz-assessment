from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from app.core.database import MongoDB
from app.graphql.context import GraphQLContext
from app.graphql.schema import schema
from app.api.routes import auth

async def get_context(request: Request):
    """
    Factory function for creating the GraphQL context.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        GraphQLContext: The initialized context
    """
    return GraphQLContext(request)


def create_app() -> FastAPI:
    """
    Application factory pattern.
    
    Configures event handlers, routers, and GraphQL.
    
    Returns:
        FastAPI: The initialized application instance
    """
    app = FastAPI()
    app.add_event_handler("startup", MongoDB.connect)
    app.add_event_handler("shutdown", MongoDB.close)

    app.include_router(auth.router, prefix="/api")
    graphql_app = GraphQLRouter(schema, context_getter=get_context)
    app.include_router(graphql_app, prefix="/api/graphql")
    return app