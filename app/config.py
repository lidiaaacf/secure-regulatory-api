from pydantic import BaseSettings

class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    API_PREFIX: str = "/api"

settings = Settings()