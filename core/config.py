from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./course.db"
    db_echo: bool = True


settings = Setting()
