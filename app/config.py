import os
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./portfolio.db"
    secret_key: str = "change-this-to-a-random-secret-key"
    app_name: str = "AI Developer Portfolio"
    debug: bool = True
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_to: str = ""
    email_from: str = ""

    class Config:
        env_file = ".env"


settings = Settings()

# Auto-detect: use SQLite if PostgreSQL is not available or if DB file is set
if settings.database_url and "postgresql" in settings.database_url:
    import os
    db_host = settings.database_url.split("@")[-1].split(":")[0] if "@" in settings.database_url else "localhost"
    # If we can't reach PostgreSQL, fall back to SQLite
    if os.name == "nt":  # Windows - likely no PG
        settings.database_url = "sqlite+aiosqlite:///./portfolio.db"

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "app" / "static" / "uploads" / "cv"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
