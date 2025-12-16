import strawberry


@strawberry.type
class GameType:
    id: str
    name: str
    type: str
    publisher_name: str
    external_game_id: str
    description: str | None = None
    is_featured: bool = False
    cover_image_url: str
    created_at: str | None = None
    updated_at: str | None = None
    likes: list[str] = strawberry.field(default_factory=list)
    trailer: str | None = None
    collage: list[str] = strawberry.field(default_factory=list)

@strawberry.input
class GameInput:
    name: str
    type: str
    publisher_name: str
    external_game_id: str
    description: str | None = None
    is_featured: bool = False
    cover_image_url: str
    trailer: str | None = None
    likes: list[str] = strawberry.field(default_factory=list)
    collage: list[str] = strawberry.field(default_factory=list)