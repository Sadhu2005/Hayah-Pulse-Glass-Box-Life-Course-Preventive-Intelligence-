"""Runtime configuration loaded from environment / .env."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    hayah_api_host: str = "127.0.0.1"
    hayah_api_port: int = 8000
    hayah_api_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    synthetic_data_dir: str = "data/synthetic"
    random_seed: int = 42

    @property
    def data_dir(self) -> Path:
        path = Path(self.synthetic_data_dir)
        if not path.is_absolute():
            path = REPO_ROOT / path
        return path

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.hayah_api_cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
