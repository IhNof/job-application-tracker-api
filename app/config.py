from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./job_tracker.db"
    html_provider_mode: str = "disabled"
    hh_fixture_path: str = "tests/fixtures/hh_search_sample.html"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
