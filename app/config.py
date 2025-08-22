import os
from typing import Optional


class Settings:
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "test_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "test")
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "2345")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test_db")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    DB_ECHO_LOG: bool = bool(int(os.getenv("DB_ECHO_LOG", "0")))


settings = Settings()