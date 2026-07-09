from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str

    api_title: str = "Movies API"
    api_version: str = "0.1.0"

    api_key: SecretStr

    debug: bool = False


settings = Settings()
