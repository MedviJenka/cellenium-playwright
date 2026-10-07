from functools import cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    APP_ENV:              str         = Field(default='dev',            description='')
    API_VERSION:          str         = Field(default='v1',             description='')
    GOOGLE_SHEETS:        str         = Field(...,                      description='')
    OPENAI_MODEL:         str         = Field(...,                      description='')
    OPENAI_API_KEY:       str | None  = Field(default=None,             description='')
    LOGFIRE_TOKEN:        str | None  = Field(default=None,             description='')
    TEST_HEADLESS:        bool        = Field(default=True,             description='')
    CREDENTIALS_JSON:     Path        = Field(Path("credentials.json"), desription='google json credentials for accessing the sheet')


@cache
def get_config() -> Settings:
    """Load settings on first use so importing cellenium never requires a configured environment."""
    return Settings()
