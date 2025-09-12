from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb+srv://anildemirok:GAPUh09PTmLDkgTf@anil-mongo-cloud.9p4mqoe.mongodb.net/OtakuTime?retryWrites=true&w=majority&tls=true"
    database_name: str = "OtakuTime"
    anime_collection: str = "AnimeReviews"
    manga_collection: str = "MangaReviews"
    user_collection: str = "Users"

    SECRET_KEY : str = "12345"
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int =  30
    ISSUER : str = "OTAKUTIME"
    AUDIENCE : str = "OTAKUTIME_USERS"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()