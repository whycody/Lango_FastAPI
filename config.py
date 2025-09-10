from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8001
    mongo_uri: str

    class Config:
        env_file = ".env"

settings = Settings()