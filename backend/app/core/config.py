"""
Application configuration — reads from environment variables.
All secrets come from .env (local) or platform env vars (Render/Vercel).
Never hardcode secrets here.
"""
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "TI Investigation Platform"
    app_version: str = "0.1.0"
    debug: bool = False

    # Supabase — required in production
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    # CORS — frontend origins allowed to call the API
    # Accepts comma-separated string from env var, e.g.:
    # CORS_ORIGINS=https://ti-platform.vercel.app,http://localhost:5173
    cors_origins: list[str] = ["http://localhost:5173"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: object) -> list[str]:
        # If the env var is a plain string, split by comma
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v  # type: ignore[return-value]

    # Security
    # Minimum response time in ms — prevents timing attacks (see SECURITY-MODEL §4)
    min_response_ms: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Single shared instance — import this everywhere
settings = Settings()
