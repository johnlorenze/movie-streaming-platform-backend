from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()

# Validate configuration at startup
WEAK_SECRET_KEYS = ["secret", "changeme", "please-change-me", "dev", "development", "test", "testing"]

if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:
    raise ValueError(
        "SECRET_KEY must be at least 32 characters long. "
        "Please set a strong SECRET_KEY in your .env file."
    )

if settings.SECRET_KEY.lower() in WEAK_SECRET_KEYS:
    raise ValueError(
        "SECRET_KEY is using a common weak value. "
        "Please set a strong, unique SECRET_KEY in your .env file."
    )

ALLOWED_ALGORITHMS = ["HS256", "HS384", "HS512", "RS256"]
if settings.ALGORITHM not in ALLOWED_ALGORITHMS:
    raise ValueError(
        f"ALGORITHM must be one of {ALLOWED_ALGORITHMS}. "
        f"Got: {settings.ALGORITHM}"
    )

if not isinstance(settings.ACCESS_TOKEN_EXPIRE_MINUTES, int) or not (1 <= settings.ACCESS_TOKEN_EXPIRE_MINUTES <= 10080):
    raise ValueError(
        "ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer between 1 and 10080 (one week). "
        f"Got: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}"
    )