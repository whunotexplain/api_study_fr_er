from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/course.db"
    db_echo: bool = True


settings = Setting()
