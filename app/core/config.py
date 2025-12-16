from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Funz App"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "funz"
    jwt_secret: str = "appsecret"
    jwt_app_id: str = "appid"
    jwt_algorithm: str = "HS256"



settings = Settings()
