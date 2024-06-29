from pathlib import Path

from pydantic_settings import BaseSettings

FILE = Path(__file__)
ROOT = FILE.parent.parent


class Settings(BaseSettings):
    # API SETTINGS
    HOST: str
    PORT: int
    CORS_ORIGINS: list
    CORS_HEADERS: list

    class Config:
        env_file = ROOT / ".env"


settings = Settings()
