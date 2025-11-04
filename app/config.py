from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "Test Webhook App"

    CALLBACK_URL: str

    COOKIE_FILE: str = "data/cookies.jar"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_SQLITE_URI(self) -> str:
        return "sqlite+aiosqlite:///./data/test_webhook.db"


settings = Settings()  # type: ignore
