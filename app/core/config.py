from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "supply-chain-intelligence-platform"
    app_version: str = "1.0.0"
    environment: str = "development"

    database_url: str

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "supplychain_knowledge"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()