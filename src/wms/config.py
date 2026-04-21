from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    brand_name: str = "The Wildcard Project"
    hashtag: str = "#WildcardCapture"
    database_url: str = "sqlite:///./wildcard.db"


settings = Settings()
