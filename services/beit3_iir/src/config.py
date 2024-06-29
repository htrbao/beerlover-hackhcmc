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

    # MODEL SETTINGS
    MODEL_NAME: str = "ViT-B/32"
    DEVICE: str = "cpu"

    # FAISS DATABASE SETTINGS
    INDEX_FILE_PATH: str
    INDEX_SUBFRAMES_FILE_PATH: str
    BEER_JSON_PATH: str
    SUBFRAMES_GROUPS_JSON_PATH: str

    class Config:
        env_file = ROOT / ".env"


settings = Settings()
