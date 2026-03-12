"""
Application configuration — reads from .env file.
"""

from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Database
    MYSQLHOST: str = "localhost"
    MYSQLUSER: str = "root"
    MYSQLPASSWORD: str = "password"
    MYSQLPORT: str = "3306"
    MYSQLDATABASE: str = "lexram_db"
    DATABASE_URL: str = ""

    def get_database_url(self) -> str:
        url = self.DATABASE_URL
        if url:
            if url.startswith("mysql://"):
                url = url.replace("mysql://", "mysql+pymysql://", 1)
            return url
        return f"mysql+pymysql://{self.MYSQLUSER}:{self.MYSQLPASSWORD}@{self.MYSQLHOST}:{self.MYSQLPORT}/{self.MYSQLDATABASE}"

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Uploads
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    MAX_FILE_SIZE_MB: int = 10

    # AI
    GEMINI_API_KEY: str = ""

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    def get_allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
if not settings.DATABASE_URL:
    settings.DATABASE_URL = settings.get_database_url()
