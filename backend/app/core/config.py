"""
Application configuration — reads from environment variables.
All secrets come from .env (local) or platform env vars (Render/Vercel).
Never hardcode secrets here.
"""
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

    # CORS — comma-separated string from env var
    # e.g. CORS_ORIGINS=https://ti-platform.vercel.app,http://localhost:5173
    cors_origins: str = "http://localhost:5173"

    def get_cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

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
