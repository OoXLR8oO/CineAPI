from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str

    API_TITLE: str = "Movies API"
    API_VERSION: str = "0.1.0"

    DEBUG: bool = False


settings = Settings()
